import datetime
import re
from dataclasses import dataclass
from enum import IntEnum
from typing import Generator

from openpyxl import load_workbook

from rtu_schedule_parser.excel_formatter import ExcelFormatter
from rtu_schedule_parser.formatter import Formatter
from rtu_schedule_parser.schedule import Lesson
from rtu_schedule_parser.schedule_data import ScheduleData
from rtu_schedule_parser.utils.academic_calendar import AcademicCalendar, Weekday


class ColumnDataType(IntEnum):
    """
    Значения основаны на смещениях колонок для группы относительно названия группы:

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
class LessonCell:
    """
    Информация о ячейке с расписанием занятий.
    """

    weekday: Weekday
    num: int  # Номер пары
    time_start: datetime.time  # Время начала занятия
    time_end: datetime.time  # Время окончания занятия
    week: int  # Чётность недели. 1 - нечётная, 2 - чётная
    row_index: int  # Индекс строки в таблице


class ExcelScheduleParser:
    RE_GROUP_NAME = re.compile(r"([А-Яа-я]{4}-\d{2}-\d{2})")

    def __init__(
        self, document_path: str, formatter: Formatter = ExcelFormatter()
    ) -> None:
        self.__document_path = document_path
        self.__formatter = formatter
        self.__workbook = None
        self.__worksheet = None

    def __open_worksheet(self):
        self.__workbook = load_workbook(self.__document_path)
        self.__worksheet = self.__workbook.active

    def __get_group_columns(self, group_row_index: int) -> list[tuple[str, int]]:
        """
        Возвращает названия групп и номера колонок для них
        """
        group_columns = []

        for row in self.__worksheet.iter_rows(group_row_index):
            for cell in row:
                if self.RE_GROUP_NAME.match(str(cell.value)):
                    group_columns.append((cell.value, cell.col_idx))

        return group_columns

    def __find_group_row(self) -> int | None:
        """
        Поиск строки с названием группы
        """
        for row in self.__worksheet.iter_rows(max_row=20, max_col=50):
            for cell in row:
                if self.RE_GROUP_NAME.match(str(cell.value)):
                    return cell.row

        return None

    def __get_lesson_elements(
        self, lesson_length: int, lesson_index: int, elements: list[str]
    ) -> str:
        """
        Получить элементы для занятия. Бывает такое, что в расписании количество предметов не равно количеству
        преподавателей или аудиторий, или видов занятий. Например, если у нас написан один предмет, но две аудитории и два преподавателя,
        то занятие будет проходить по подгруппам в разных аудиториях.
        """
        if lesson_length == len(elements):
            return elements[lesson_index]
        elif len(elements) == 1:
            return elements[0]
        else:
            return elements[lesson_length]

    def __parse_lessons(
        self, group_column: int, lesson_cells: list[LessonCell]
    ) -> Generator[Lesson, None, None]:
        """
        Парсинг занятий.
        """
        for lesson_cell in lesson_cells:
            row = self.__worksheet[lesson_cell.row_index]

            subjects = row[group_column + ColumnDataType.SUBJECT].value
            types = row[group_column + ColumnDataType.TYPE].value
            teachers = row[group_column + ColumnDataType.TEACHER].value
            rooms = row[group_column + ColumnDataType.ROOM].value

            lesson_names = self.__formatter.get_lessons(subjects)
            self.__formatter.get_types(types)
            self.__formatter.get_teachers(teachers)
            self.__formatter.get_rooms(rooms)

            # стоит ли предмет на чётных неделях
            is_even_week = lesson_cell.week % 2 == 0

            self.__formatter.get_weeks(
                subjects, is_even_week, AcademicCalendar.MAX_WEEKS
            )

            lessons_len = len(lesson_names)

            for i in range(lessons_len):
                yield Lesson(
                    lesson_cell.weekday,
                    lesson_cell.num,
                    lesson_cell.time_start,
                    lesson_cell.time_end,
                    self.__get_lesson_elements(lessons_len, i, lesson_names),
                    self.__get_lesson_elements(lessons_len, i, self.__formatter.types),
                    self.__get_lesson_elements(lessons_len, i, self.__formatter.teachers),
                    self.__get_lesson_elements(lessons_len, i, self.__formatter.rooms),
                )


def __get_lesson_cells(
    self, group_cell_index: int, group_row_index: int
) -> Generator[LessonCell, None, None]:
    """
    Возвращает ячейки с расписанием занятий.
    """

    # После строки с названием групп идет заголовочная строка с названиями колонок
    initial_row_num = group_row_index + 2

    row_count = self.__worksheet.max_row
    row_count = 150 if row_count > 150 else row_count

    weekday, lesson_num, time_start, time_end = None, None, None, None

    group_cell_index -= 1
    for i in range(initial_row_num, row_count):
        # Информация о чётности недели на каждой строке, остальное через строку,
        # поэтому чётность недели находим в каждой итерации
        #
        # +---+------+-------+----+
        # | 1 | 9-00 | 10-30 | I  |
        # +---+------+-------+----+
        # |   |      |       | II |
        # +---+------+-------+----+

        week = None

        row = self.__worksheet[i]

        weekday_cell_value = row[group_cell_index + ColumnDataType.WEEKDAY].value
        lesson_num_cell_value = row[
            group_cell_index + ColumnDataType.LESSON_NUMBER
        ].value
        start_time_cell_value = row[group_cell_index + ColumnDataType.START_TIME].value
        end_time_cell_value = row[group_cell_index + ColumnDataType.END_TIME].value
        week_cell_value = row[group_cell_index + ColumnDataType.WEEK].value

        try:
            if weekday_cell_value:
                weekday = Weekday.get_weekday_by_name(weekday_cell_value.lower())

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
                yield LessonCell(weekday, lesson_num, time_start, time_end, week, i)

        except ValueError:
            pass

    def parse(self) -> ScheduleData:
        self.__open_worksheet()

        group_name_row = self.__find_group_row()
        if group_name_row is None:
            raise Exception("The row with the group name was not found")

        group_columns = self.__get_group_columns(group_name_row)

        first_group_column = group_columns[0][1]
        lesson_cells = list(self.__get_lesson_cells(first_group_column, group_name_row))
        print(lesson_cells)


if __name__ == "__main__":
    parser = ExcelScheduleParser(
        "C:\\Users\\foran\\Downloads\\ИИТ_2 курс_21-22_весна_очка.xlsx"
    )
    parser.parse()
