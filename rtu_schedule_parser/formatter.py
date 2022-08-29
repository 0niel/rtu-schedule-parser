from __future__ import annotations

from abc import ABCMeta, abstractmethod

from rtu_schedule_parser.constants import LessonType


class Formatter(metaclass=ABCMeta):
    """Приведение значений ячеек таблицы расписания к нужному формату.

    Methods
    -------
    get_lesson(self, lesson: str)
        Получение названия предмета.
    get_room(self, rooms: str)
        Получение списка аудиторий проведения занятия.
    get_teacher(self, teachers_names: str)
        Получение списка преподавателей.
    get_weeks(self, lesson: str)
        Получения списка недель, на которых проходит занятие.
    """

    @abstractmethod
    def get_lessons(
        self, lesson: str
    ) -> list[tuple[str, LessonType | None, int | None]]:
        """
        Метод должен получать значение ячейки документа, в котором
        хранится информация о проводимой дисциплине занятия. Параметр
        lesson может содержать дополнительную информацию. Например,
        lesson может состоять из списка недель, времени и аудитории.
        Метод должен вернуть исключительно список названий предметов.

        Args:
            lesson (str): значение ячейки из таблицы документа

        Returns:
        ----------
            Примеры правильных реализаций метода:

            ("1,5,9,13 н Оперционные системы\n3,7,11,15 н  Оперционные системы")
                return ['Оперционные системы', 'Оперционные системы']
            get_lesson("1,5,9 н. Мат. анализ\n3, 7, 11 н.  Линейная алгебра")
                return ['Мат. анализ', 'Линейная алгебра']
            get_lesson("21,22 н. Проектирование 18:10-19:40 ауд. Д Башлыкова А.А.")
                return ['Проектирование']
        """
        raise NotImplementedError

    @abstractmethod
    def get_rooms(self, rooms: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_teachers(self, teachers_names: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_weeks(
        self, lesson: str, is_even: bool | None = None, max_weeks=None
    ) -> list[list[int]]:
        """Метод должен получать списки недель, на которых предмет проводится.
        Если в одной ячейке несколько предметов, то метод должен вернуть несколько
        списков с неделями, для каждого предмета свой. При возврате списка недель
        необходимо учитывать чётность (is_even) и максимальное количество недель
        в семестре (max_weeks).

        Args:
            lesson (str): значение ячейки предмета, в которой хранится название
            предмета и недели проведения занятия.
            is_even (boolean, optional): True, если предмет проводится только по
            чётным неделям и False, если по нечётным. Если None, то чётность недели
            не важна (проводится на всех неделях). По умолчанию None.
            max_weeks (int, optional): Максимальное количество недель в семестре.
            Необходимо для тех случаев, когда у предмета список недель не указан,
            т.е. когда предмет проводится на всех неделях семестра. По умолчанию
            None.

        Returns:
        ----------
            Возвращает список, состоящий из списков недель. Каждый список
            соотвествует одному проводимому предмету.

            Примеры правильных реализаций метода:

            get_weeks("1,5,9,13 н Оперционные системы\n3,7,11,15 н  Оперционные системы", False)
                return [[1, 5, 9, 13],[3, 7, 11, 15]]
            get_weeks("1,5,9 н. кр. 5 нед. Мат. анализ")
                return [[1, 9]]
        """
        raise NotImplementedError

    @abstractmethod
    def get_types(self, cell: str) -> list[LessonType]:
        raise NotImplementedError
