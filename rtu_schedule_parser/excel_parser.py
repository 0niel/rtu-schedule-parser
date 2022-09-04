from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Generator

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

import rtu_schedule_parser.utils.academic_calendar as academic_calendar
from rtu_schedule_parser import ScheduleParser
from rtu_schedule_parser.constants import Degree, Institute
from rtu_schedule_parser.formatter import Formatter
from rtu_schedule_parser.schedule import Lesson, LessonEmpty, Schedule
from rtu_schedule_parser.schedule_data import ScheduleData

__all__ = ["ExcelScheduleParser"]


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
class _LessonCell:
    """Represents a cell in the schedule table."""

    weekday: academic_calendar.Weekday
    num: int  # The number of the lesson
    time_start: datetime.time  # The start time of the lesson
    time_end: datetime.time  # The end time of the lesson
    week: int  # Parity of the week. 1 - odd, 2 - even
    row_index: int  # Index of the row in the table


class ExcelScheduleParser(ScheduleParser):
    # Group name regex pattern
    RE_GROUP_NAME = re.compile(r"([А-Яа-я]{4}-\d{2}-\d{2})")

    def __init__(
        self,
        document_path: str,
        formatter: Formatter,
        course: int,
        period: academic_calendar.Period,
        institute: Institute,
        degree: Degree,
    ) -> None:
        super().__init__(document_path, formatter, course, period, institute, degree)

        self.__workbook = None
        self.__worksheets = None

    def __open_worksheets(self):
        self.__workbook = load_workbook(self._document_path)
        self.__worksheets = self.__workbook.worksheets

    def __get_group_columns(
        self, group_row_index: int, worksheet: Worksheet
    ) -> list[tuple[str, int]]:
        """Returns a list of tuples containing the group name and the column index for each group in the table."""
        group_columns = []

        for row in worksheet.iter_rows(group_row_index):
            for cell in row:
                if self.RE_GROUP_NAME.match(str(cell.value)):
                    group_columns.append((cell.value, cell.col_idx))

        return group_columns

    def __find_group_row(self, worksheet) -> int | None:
        """Find the row containing the group name."""
        for row in worksheet.iter_rows(max_row=20, max_col=50):
            for cell in row:
                if self.RE_GROUP_NAME.match(str(cell.value)):
                    return cell.row

        return None

    def __get_lesson_element(
        self, lesson_length: int, lesson_index: int, elements: list[Any]
    ) -> Any:
        """
        Returns the element (room, teacher, etc.) for the lesson. If the lessons length is greater than 1,
        then the element is repeated for each lesson. If the element is not specified, then the element is empty. If
        the element is specified for only one lesson, then the element is repeated for all lessons.
        """
        if lesson_length == len(elements):
            return elements[lesson_index]
        elif len(elements) == 1:
            return elements[0]
        elif len(elements) == 0:
            return None
        else:
            raise ValueError("Invalid lesson length")

    def __parse_lessons(
        self, group_column: int, lesson_cells: list[_LessonCell], worksheet: Worksheet
    ) -> Generator[Lesson | LessonEmpty, None, None]:
        """
        Parses the lessons for the group. The lessons are parsed from the table in the worksheet. The lessons are
        parsed from the cells specified in the lesson_cells list. The lessons are parsed for the group in the
        column specified by the group_column parameter.
        """
        group_column -= 1
        for lesson_cell in lesson_cells:
            row = worksheet[lesson_cell.row_index]

            subjects = row[group_column + _ColumnDataType.SUBJECT].value
            types = row[group_column + _ColumnDataType.TYPE].value
            teachers = str(row[group_column + _ColumnDataType.TEACHER].value)
            rooms = row[group_column + _ColumnDataType.ROOM].value

            if subjects is None or subjects == "":
                yield LessonEmpty(
                    lesson_cell.num,
                    lesson_cell.weekday,
                    lesson_cell.time_start,
                    lesson_cell.time_end,
                )
            else:
                is_even_week = lesson_cell.week % 2 == 0

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
                    lesson_teachers = lesson_teachers if lesson_teachers else []

                    yield Lesson(
                        lesson_cell.num,
                        lesson_names[i][0],
                        lesson_weeks[i],
                        lesson_cell.weekday,
                        lesson_teachers,
                        lesson_cell.time_start,
                        lesson_cell.time_end,
                        lesson_names[i][1] or lesson_type,
                        lesson_room,
                        lesson_names[i][2],
                    )

    def __get_lesson_cells(
        self, group_cell_index: int, group_row_index: int, worksheet: Worksheet
    ) -> Generator[_LessonCell, None, None]:
        """
        Returns a list of `_LessonCell` objects. The list contains the cells in the table that contain the lessons.
        """

        # Header line with the names of the columns after the group name
        initial_row_num = group_row_index + 2

        row_count = worksheet.max_row
        row_count = 150 if row_count > 150 else row_count

        weekday, lesson_num, time_start, time_end = None, None, None, None

        group_cell_index -= 1
        for i in range(initial_row_num, row_count):
            # The parity of the week is determined by the row number in the table. The rest through the line, so
            # find the parity of the week in each iteration (row).
            #
            # +---+------+-------+----+
            # | 1 | 9-00 | 10-30 | I  |
            # +---+------+-------+----+
            # |   |      |       | II |
            # +---+------+-------+----+

            week = None

            row = worksheet[i]

            weekday_cell_value = row[group_cell_index + _ColumnDataType.WEEKDAY].value
            lesson_num_cell_value = row[
                group_cell_index + _ColumnDataType.LESSON_NUMBER
            ].value
            start_time_cell_value = row[
                group_cell_index + _ColumnDataType.START_TIME
            ].value
            end_time_cell_value = row[group_cell_index + _ColumnDataType.END_TIME].value
            week_cell_value = row[group_cell_index + _ColumnDataType.WEEK].value

            try:
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
                    yield _LessonCell(
                        weekday, lesson_num, time_start, time_end, week, i
                    )

            except ValueError:
                pass

    def parse(self) -> ScheduleData:
        self.__open_worksheets()

        schedule = []

        for worksheet in self.__worksheets:
            group_name_row = self.__find_group_row(worksheet)
            if group_name_row is None:
                raise Exception("The row with the group type_name was not found")

            group_columns = self.__get_group_columns(group_name_row, worksheet)

            first_group_column = group_columns[0][1]
            lesson_cells = list(
                self.__get_lesson_cells(first_group_column, group_name_row, worksheet)
            )

            for group_column in group_columns:
                lessons = list(
                    self.__parse_lessons(group_column[1], lesson_cells, worksheet)
                )
                group_name = group_column[0]
                schedule.append(
                    Schedule(
                        group_name,
                        lessons,
                        self._course,
                        self._period,
                        self._institute,
                        self._degree,
                    )
                )

        return ScheduleData(schedule)
