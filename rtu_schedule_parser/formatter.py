from __future__ import annotations

from abc import ABCMeta, abstractmethod

from rtu_schedule_parser.constants import LessonType
from rtu_schedule_parser.schedule import Room


class Formatter(metaclass=ABCMeta):
    """Приведение значений ячеек таблицы расписания к нужному формату."""

    @abstractmethod
    def get_lessons(
        self, lessons_cell_value: str
    ) -> list[tuple[str, LessonType | None, int | None]]:
        """
        Получить информацию о предмете, его типе и подгруппе из ячейки таблицы расписания.

        Args:
            lessons_cell_value: Значение ячейки таблицы расписания.

        Returns: Список кортежей вида (предмет, тип предмета, подгруппа). Тип предмета или подгруппа могут быть не
        заданы в ячейке, тогда им будут соответствовать None.

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
        Получение аудиторий из значения ячейки документа, в котором хранится информация об аудиториях занятия.

        Args:
            rooms_cell_value: значение ячейки из таблицы документа

        Returns: Список аудиторий занятия. Если аудиторий нет, то возвращается пустой список. Обычно каждому предмету
        соответствует одна аудитория.
        """
        raise NotImplementedError

    @abstractmethod
    def get_teachers(self, names_cell_value: str) -> list[str]:
        """
        Получение имен преподавателей из значения ячейки документа, в котором хранится информация о преподавателях
        занятия.

        Args:
            names_cell_value: значение ячейки из таблицы документа

        Returns: Список имен преподавателей занятия. Если преподавателей нет, то возвращается пустой список. Обычно
        каждому предмету соответствует один преподаватель.
        """
        raise NotImplementedError

    @abstractmethod
    def get_weeks(
        self, lesson: str, is_even: bool | None = None, max_weeks: bool | int = None
    ) -> list[list[int]]:
        """Возвращает список недель, на которых проводится занятие, учитывая чётность и максимальное кол-во недель.
        Каждому предмету должен соответствовать список недель. Если предметов нет, то возвращается пустой список.

        Args:
            lesson: значение ячейки дисциплин из таблицы документа is_even: True, если предмет проводится только по
            чётным неделям и False, если по нечётным. Если None, то чётность недели не важна (проводится на всех
            неделях). По умолчанию None.

            max_weeks: Максимальное количество недель в семестре. Необходимо для тех
            случаев, когда у предмета список недель не указан, т.е. когда предмет проводится на всех неделях семестра. По
            умолчанию None.

        Examples:
            >>> from rtu_schedule_parser.excel_formatter import ExcelFormatter
            >>> formatter = ExcelFormatter()
            >>> formatter.get_weeks("1,5,9,13 н Оперционные системы\\n3,7,11,15 н  Оперционные системы", is_even=False)
            [[1, 5, 9, 13],[3, 7, 11, 15]]
            >>> formatter.get_lessons("1,5,9 н. кр. 5 нед. Мат. анализ")
            [[1, 9]]
        """
        raise NotImplementedError

    @abstractmethod
    def get_types(self, types_cell_value: str) -> list[LessonType]:
        """
        Получение типов занятий из значения ячейки документа, в котором хранится информация о типах занятий.

        Args:
            types_cell_value: значение ячейки из таблицы документа

        Returns: Список типов занятий занятия. Обычно каждому предмету соответствует один тип занятия. Если предметов
        нет, то возвращается пустой список. У некоторых предметов может не быть типа занятия. Предмету не может
        соответствовать несколько типов занятий.
        """
        raise NotImplementedError
