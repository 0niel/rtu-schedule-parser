from enum import Enum, IntEnum


class Degree(IntEnum):
    BACHELOR = 1
    MASTER = 2
    PHD = 3
    COLLEGE = 4


class RoomType(IntEnum):
    """Перечисление возможных типов аудиторий."""

    __slots__ = ()

    # Тип аудиторий по умолчанию. Используется для лекций и практик.
    AUDITORY = 1

    # Аудитория с компьютерами.
    COMPUTERS = 2

    # Аудитория для лабораторных работ.
    LABORATORY = 3

    # Дистанционно (в СДО).
    DISTANTLY = 4

    # Спортивный зал (физкультура).
    SPORT = 5


class LessonType(Enum):
    """Перечисление возможных типов занятий."""

    __slots__ = ()

    PRACTICE = "пр"
    LECTURE = "лек"
    INDIVIDUAL_WORK = "с/р"
    LABORATORY_WORK = "лаб"


class ScheduleType(IntEnum):
    """
    Перечисление типов документов расписания.
    """

    __slots__ = ()

    # Стандартный документ расписания на семестр
    SEMESTER = 1

    # Документ расписания зачётной сессии. Имеет вид как стандартный
    # документ, но расписание только одной недели (зачётной)
    TEST_SESSION = 2

    # Документ расписания экзаменационной сессии
    EXAM_SESSION = 3


class Institute(Enum):
    """
    Перечисление возможны учебных подразделений.

    Подробный список: https://www.mirea.ru/education/the-institutes-and-faculties/
    """

    __slots__ = ()

    IIT = ("ИИТ", "Институт информационных технологий")

    III = ("ИИИ", "Институт искусственного интеллекта")

    IKB = ("ИКБ", "Институт кибербезопасности и цифровых технологий")

    IPTIP = (
        "ИПТИП",
        "Институт перспективных технологий и индустриального программирования",
    )

    IRI = ("ИРИ", "Институт радиотехники и электроники")

    ITU = ("ИТУ", "Институт технологий управления")

    ITHT = ("ИТХТ", "Институт тонких химических технологий им. М.В. Ломоносова")

    @property
    def short_name(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]

    @staticmethod
    def get_by_name(name):
        for institute in Institute:
            if institute.name == name:
                return institute
        raise ValueError(f"Unknown institute name: {name}")

    @staticmethod
    def get_by_short_name(short_name):
        for institute in Institute:
            if institute.short_name == short_name:
                return institute
        raise ValueError(f"Unknown institute short name: {short_name}")


class Campus(Enum):
    """
    Перечисление возможных кампусов, в которых может проводиться занятие.
    """

    __slots__ = ()

    MP_1 = "ул. Малая Пироговская, д.1"
    V_78 = "Проспект Вернадского, д.78"
    V_86 = "Проспект Вернадского, д.86"
    S_20 = "ул. Стромынка, 20"
    SG_22 = "5-я ул. Соколиной горы, д.22"
