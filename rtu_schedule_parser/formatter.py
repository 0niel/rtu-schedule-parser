from __future__ import annotations

from abc import ABCMeta, abstractmethod

from rtu_schedule_parser.constants import LessonType
from rtu_schedule_parser.schedule import Room


class Formatter(metaclass=ABCMeta):
    """Abstract class for formatting schedule data."""

    @abstractmethod
    def get_lessons(
        self, lessons_cell_value: str
    ) -> list[tuple[str, LessonType | None, int | None]]:
        """
        Get information about the subject, its type and subgroup from the schedule table cell.

        Args:
            lessons_cell_value: The value of the schedule table cell.

        Returns:
            A list of tuples containing information about the subject, its type and subgroup. The type or
            subgroup may not be specified in the table cell. In this case, the value will be None.

        Examples:
            >>> from rtu_schedule_parser.excel_formatter import ExcelFormatter
            >>> formatter = ExcelFormatter()
            >>> formatter.get_lessons("кр. 3,5 н. Теория автоматического управления")
            [('Теория автоматического управления', None, None)]
            >>> formatter.get_lessons("2,6,10,14 н Экология\\n4,8,12,16 Правоведение")
            [('Экология', None, None), ('Правоведение', None, None)]
            >>> formatter.get_lessons("1,5,9,13 н. Физика (1 п/г)\\n1,5,9,13 н. Физика (2 п/г)")
            [('Физика', None, 1), ('Физика', None, 2)]

        """
        raise NotImplementedError

    @abstractmethod
    def get_rooms(self, rooms_cell_value: str) -> list[Room]:
        """
        Get information about the room from the schedule table cell value.

        Args:
            rooms_cell_value: The value of the schedule table cell.

        Returns:
            A list of Room objects. If the room is not specified in the table cell, the list will be empty. If
            the room is specified, but the campus or room type is not specified, the value will be None. Usually each
            schedule subject has only one room, but sometimes there are two or more rooms for one subject. For example,
            in the case of a laboratory.
        """
        raise NotImplementedError

    @abstractmethod
    def get_teachers(self, names_cell_value: str) -> list[str] | list[tuple[str, int]]:
        """
        Get information about the teacher from the schedule table cell value.

        Args:
            names_cell_value: The value of the schedule table cell.

        Returns:
            A list of teacher names. If the teacher is not specified in the table cell, the list will be empty.
            Usually each schedule subject has only one teacher, but sometimes there are two or more teachers for one
            subject. For example, in the case of a laboratory. Usually the teacher's type_name is specified in the form
            of a surname and initials. For example, "Иванов И.И.". The names are returned in a normalized form. For
            example, "Иванов И. И" will be returned as "Иванов И.И.", and "И.И. Иванов" will be returned as
            "Иванов И.И.".

            If names_cell_value contains a subgroup number, the return value will be a list of tuples. The first
            element of the tuple is the teacher's name, and the second element is the subgroup number. For example,
            "Казачкова О.А.,1 пг\nКазачкова О.А.,2 пг" will be returned as
            [("Казачкова О.А.", 1), ("Казачкова О.А.", 2)].
        """
        raise NotImplementedError

    @abstractmethod
    def get_weeks(
        self, lesson: str, is_even: bool | None = None, max_weeks: bool | int = None
    ) -> list[list[int]]:
        """Get information about the weeks from the schedule table cell value and the parity of the week.
        Return a list of lists of weeks. Each list contains the weeks for one subject. It is necessary to take into
        account those weeks that are specified in the lesson cell and those that are specified in the parity of the
        week. For example, the lesson cell may contain the following value: "1,5,9,13 н. Физика (1 п/г)". In this case,
        if the parity of the week is not specified, the weeks will be [1, 5, 9, 13]. If `is_even` is True, the weeks
        will be [[]] (empty list). The subject must neccesarily correspond at least one week.

        Args:

            lesson: The value of the schedule lesson table cell. For example, "1,5,9,13 н. Физика (1 п/г)". The lesson
                cell value may not contain a weeks value. For example, "Физика (1 п/г)". In this case, the subject will
                correspond to all weeks, considering the parity of the week. The lesson cell value may also contain a
                list of weeks in which subject is not held. For example, "кр. 3,5 н. Теория автоматического управления".
                In this case, the subject will correspond to all weeks except 3 and 5, considering the parity of the
                week.


            is_even: The parity of the week. If the value is True, the subject will correspond to even weeks. If the
                value is False, the subject will correspond to odd weeks. If the value is None, the subject will
                correspond to all weeks. The default value is None.

            max_weeks: The maximum number of weeks in the semester. It is necessary for those cases when the weeks
                are not explicitly specified in the lesson cell value. For example, "Физика (1 п/г)". In this case,
                the subject will correspond to all weeks, considering the parity of the week and the weeks of exce . It
                is necessary to take into account the fact that the number of weeks in the semester may be different.
                For example, in the first semester, the number of weeks is 16, and in the second semester, the number of
                weeks is 17. The default value is None.

        Returns:
            A list of lists of weeks. Each list contains the weeks for one subject.

        Examples:
            >>> from rtu_schedule_parser.excel_formatter import ExcelFormatter
            >>> formatter = ExcelFormatter()
            >>> formatter.get_weeks("1,5,9,13 н Оперционные системы\\n3,7,11,15 н  Оперционные системы", is_even=False)
            [[1, 5, 9, 13], [3, 7, 11, 15]]
            >>> formatter.get_weeks("1,5,9 н. кр. 5 нед. Мат. анализ")
            [[1, 9]]
        """
        raise NotImplementedError

    @abstractmethod
    def get_types(self, types_cell_value: str) -> list[LessonType]:
        """
        Get information about the lesson type from the schedule table cell value.

        Args:
            types_cell_value: The value of the schedule table cell.

        Returns:
            A list of `LessonType` objects. If the lesson type is not specified in the table cell, the list will be
            empty. If the subject is specified, but the lesson type is not specified, the value will be None. One lesson
            cannot have more than one lesson type. Usually the lesson type is specified in the form of a short
            type_name. For example, "лаб". Some lessons may not have a lesson type.
        """
        raise NotImplementedError
