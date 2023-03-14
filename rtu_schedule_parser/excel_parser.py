from __future__ import annotations

import contextlib
import datetime
import logging
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Generator

from openpyxl.worksheet.worksheet import Worksheet

import rtu_schedule_parser.utils.academic_calendar as academic_calendar
from rtu_schedule_parser.constants import Degree, Institute, ScheduleType
from rtu_schedule_parser.excel_formatter import ExcelFormatter
from rtu_schedule_parser.parser import ScheduleParser
from rtu_schedule_parser.schedule import Lesson, LessonEmpty, LessonsSchedule
from rtu_schedule_parser.schedule_data import ScheduleData

__all__ = ["ExcelScheduleParser"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _ColumnDataType(IntEnum):
    """
    Used to determine the type of data in the column. The order of the values is important.

    The values are based on the column offset from the group name column:
    +-------------+--------+--------------+---------------+--------+---------+-------------+-------------------+--------+
    |             |        |              |               |        | ГРУППА  |             |                   |        |
    +-------------+--------+--------------+---------------+--------+---------+-------------+-------------------+--------+
    | День недели | № пары | Нач.занятий  | Оконч.занятий | Неделя | Предмет | Вид занятий | ФИО преподавателя | № ауд. |
    | -5          | -4     | -3           | -2            | -1     | 0       | 1           | 2                 | 3      |
    +-------------+--------+--------------+---------------+--------+---------+-------------+-------------------+--------+
    """

    WEEKDAY = -5
    LESSON_NUMBER = -4
    START_TIME = -3
    END_TIME = -2
    WEEK = -1
    SUBJECT = 0
    TYPE = 1
    TEACHER = 2
    ROOM = 3


@dataclass
class _LessonRow:
    """Represents a cell in the schedule table."""

    weekday: academic_calendar.Weekday
    num: int  # The number of the lesson
    time_start: datetime.time  # The start time of the lesson
    time_end: datetime.time  # The end time of the lesson
    week: int  # Parity of the week. 1 - odd, 2 - even
    row: tuple[str, ...]  # The row of the table


class ExcelScheduleParser(ScheduleParser):
    def __init__(
        self,
        document_path: str,
        period: academic_calendar.Period,
        institute: Institute,
        degree: Degree,
    ) -> None:
        super().__init__(document_path, ExcelFormatter(), period, institute, degree)

    def __get_lesson_element(
        self, lesson_length: int, lesson_index: int, elements: list[Any]
    ) -> Any | None:
        """
        Returns the element (room, teacher, etc.) for the lesson. If the lessons length is greater than 1,
        then the element is repeated for each lesson. If the element is not specified, then the element is empty. If
        the element is specified for only one lesson, then the element is repeated for all lessons.
        """
        if lesson_length == len(elements):
            return elements[lesson_index]
        elif len(elements) == 1 or len(set(elements)) == 1:
            return elements[0]
        elif not elements:
            return None
        elif lesson_length == 1 and len(elements) == 2:
            return elements[0]
        elif lesson_length == 4 and len(elements) == 2:
            return elements[lesson_index // 2]
        else:
            return None

    def __parse_lessons(
        self, group_column: int, lesson_rows: list[_LessonRow], worksheet: Worksheet
    ) -> Generator[Lesson | LessonEmpty, None, None]:
        """
        Parses the lessons for the group. The lessons are parsed from the table in the worksheet. The lessons are
        parsed from the cells specified in the lesson_cells list. The lessons are parsed for the group in the
        column specified by the group_column parameter.
        """
        group_column -= 1
        for lesson_row_data in lesson_rows:
            row = lesson_row_data.row

            subjects = row[group_column + _ColumnDataType.SUBJECT].value
            types = row[group_column + _ColumnDataType.TYPE].value
            teachers = row[group_column + _ColumnDataType.TEACHER].value
            teachers = str(teachers) if teachers else ""
            rooms = row[group_column + _ColumnDataType.ROOM].value
            rooms = str(rooms) if rooms else ""

            if subjects is None or subjects.strip() == "":
                yield LessonEmpty(
                    lesson_row_data.num,
                    lesson_row_data.weekday,
                    lesson_row_data.time_start,
                    lesson_row_data.time_end,
                )
            else:
                is_even_week = lesson_row_data.week % 2 == 0

                lesson_names = self._formatter.get_lessons(subjects)
                lesson_weeks = self._formatter.get_weeks(
                    subjects, is_even_week, academic_calendar.MAX_WEEKS
                )

                if len(lesson_weeks) == 0:
                    raise ValueError("Invalid lesson weeks")

                lesson_teachers, lesson_types, lesson_rooms = None, None, None
                if teachers:
                    lesson_teachers = self._formatter.get_teachers(teachers)
                if types:
                    lesson_types = self._formatter.get_types(types)
                if rooms:
                    lesson_rooms = self._formatter.get_rooms(rooms)

                lessons_len = len(lesson_names)

                for i in range(lessons_len):
                    lesson_type = (
                        self.__get_lesson_element(lessons_len, i, lesson_types)
                        if lesson_types
                        else None
                    )
                    lesson_room = (
                        self.__get_lesson_element(lessons_len, i, lesson_rooms)
                        if lesson_rooms
                        else None
                    )

                    if lesson_room:
                        lesson_room = self._set_default_campus(lesson_room)

                    lesson_teachers = lesson_teachers or []

                    subgroup = lesson_names[i][2]

                    if len(lesson_teachers) > 0 and isinstance(
                        lesson_teachers[0], tuple
                    ):
                        if len(lesson_teachers) != lessons_len:
                            raise ValueError("Invalid lesson teachers")

                        subgroup = lesson_teachers[i][1]

                    yield Lesson(
                        lesson_row_data.num,
                        lesson_names[i][0],
                        lesson_weeks[i],
                        lesson_row_data.weekday,
                        lesson_teachers,
                        lesson_row_data.time_start,
                        lesson_row_data.time_end,
                        lesson_names[i][1] or lesson_type,
                        lesson_room,
                        subgroup,
                    )

    def __parse_lesson_cells(
        self, group_cell_index: int, group_row_index: int, worksheet: Worksheet
    ) -> Generator[_LessonRow, None, None]:
        """
        Returns a list of `_LessonRow` objects. The list contains the cells in the table that contain the lessons.
        """

        # Header line with the names of the columns after the group name
        initial_row_num = group_row_index + 2

        row_count = min(worksheet.max_row, 100)

        weekday, lesson_num, time_start, time_end = None, None, None, None

        group_cell_index -= 1  # Convert to 0-based index
        for row in worksheet.iter_rows(min_row=initial_row_num, max_row=row_count):
            # The parity of the week is determined by the row number in the table. The rest through the line, so
            # find the parity of the week in each iteration (row).
            #
            # +---+------+-------+----+
            # | 1 | 9-00 | 10-30 | I  |
            # +---+------+-------+----+
            # |   |      |       | II |
            # +---+------+-------+----+

            week = None

            weekday_cell_value = row[group_cell_index + _ColumnDataType.WEEKDAY].value
            lesson_num_cell_value = row[
                group_cell_index + _ColumnDataType.LESSON_NUMBER
            ].value
            start_time_cell_value = row[
                group_cell_index + _ColumnDataType.START_TIME
            ].value
            end_time_cell_value = row[group_cell_index + _ColumnDataType.END_TIME].value
            week_cell_value = row[group_cell_index + _ColumnDataType.WEEK].value

            with contextlib.suppress(ValueError):
                if weekday_cell_value:
                    weekday = academic_calendar.Weekday.get_weekday_by_name(
                        weekday_cell_value.lower()
                    )

                if lesson_num_cell_value:
                    lesson_num = int(lesson_num_cell_value)

                def get_time(cell_value):
                    return datetime.time(
                        hour=int(cell_value.split("-")[0]),
                        minute=int(cell_value.split("-")[1]),
                    )

                if start_time_cell_value:
                    time_start = get_time(start_time_cell_value)

                if end_time_cell_value:
                    time_end = get_time(end_time_cell_value)

                if week_cell_value == "I":
                    week = 1
                elif week_cell_value == "II":
                    week = 2

                if weekday and lesson_num and time_start and time_end and week:
                    yield _LessonRow(
                        weekday, lesson_num, time_start, time_end, week, row
                    )

    def __parse_worksheet(self, worksheet: Worksheet, force: bool = False):
        """
        Parses the worksheet and returns a list of groups.
        """
        schedule = []  # type: list[LessonsSchedule]

        group_name_row = self._find_group_row(worksheet)

        if group_name_row is None:
            return

        group_columns = self._get_group_columns(group_name_row, worksheet)

        first_group_column = group_columns[0][1]
        lesson_cells = list(
            self.__parse_lesson_cells(first_group_column, group_name_row, worksheet)
        )

        for group_column in group_columns:
            try:
                lessons = list(
                    self.__parse_lessons(group_column[1], lesson_cells, worksheet)
                )
                group_name = group_column[0]

                logger.info(
                    f"Processing group '{group_name}', worksheet '{worksheet.title}'"
                )

                schedule.append(
                    LessonsSchedule(
                        group=group_name,
                        period=self._period,
                        institute=self._institute,
                        degree=self._degree,
                        document_url=None,  # TODO: implement,
                        lessons=lessons,
                    )
                )

            except ValueError:
                if not force:
                    raise
                else:
                    logger.error(
                        f"Error parsing schedule for group {group_column[0]}"
                        f" in worksheet {worksheet.title}. Skipping."
                    )

        return schedule

    def parse(
        self,
        force: bool = False,
        generate_dataframe: bool = False,
        schedule_type: ScheduleType = ScheduleType.SEMESTER,
    ) -> ScheduleData:
        """
        Args:
            force: If True, then the schedule will be parsed even if exceptions occur during parsing.
            generate_dataframe: If True, then the schedule will be converted to a pandas DataFrame. It increases the
                parsing time.
            schedule_type: The type of schedule to parse (semester or test session for this parser).
        """

        if (
            schedule_type != ScheduleType.SEMESTER
            and schedule_type != ScheduleType.TEST_SESSION
        ):
            raise ValueError(
                "This parser supports only semester and test session schedules."
            )

        self._open_worksheets()

        schedule = []

        for worksheet in self._worksheets:
            if result := self.__parse_worksheet(worksheet, force):
                schedule.extend(result)

        return ScheduleData(schedule, generate_dataframe, schedule_type)
