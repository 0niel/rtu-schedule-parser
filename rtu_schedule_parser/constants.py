import re
from enum import Enum, IntEnum

# Regex pattern for group name validation.
RE_GROUP_NAME = re.compile(r"([А-Яа-я]{4}-\d{2}-\d{2})")


class Degree(IntEnum):
    """Enum for degree types."""

    __slots__ = ()

    BACHELOR = 1
    MASTER = 2
    PHD = 3
    COLLEGE = 4


class RoomType(Enum):
    """Enumeration of room types."""

    __slots__ = ()

    # Default room type. Usually used for lectures and seminars.
    AUDITORY = "ауд"

    # Room type with computers.
    COMPUTERS = "комп"

    # Room type for laboratories.
    LABORATORY = "лаб"

    # Room type for physical education.
    SPORT = "физ"


class LessonType(Enum):
    """Enumeration of lesson types."""

    __slots__ = ()

    PRACTICE = "пр"
    LECTURE = "лек"
    INDIVIDUAL_WORK = "с/р"
    LABORATORY_WORK = "лаб"
    TEST_SESSION = "зач"


class ScheduleType(IntEnum):
    """
    Enumeration of schedule document types.
    """

    __slots__ = ()

    # Default schedule type. Used for semester schedule.
    SEMESTER = 1

    # Document of the test session schedule. Has the same view as a standard document,
    # but the schedule is only one week.
    TEST_SESSION = 2

    # Document of the exam session schedule.
    EXAM_SESSION = 3


class ExamType(IntEnum):
    """
    Enumeration of exam types. Used in the exam schedule.
    """

    __slots__ = ()

    CONSULTATION = 1
    EXAMINATION = 2


class Institute(Enum):
    """
    Enumeration of institutes.

    Detailed information about institutes can be found here: https://www.mirea.ru/education/the-institutes-and-faculties/
    """

    __slots__ = ()

    IIT = ("ИИТ", "Институт информационных технологий")

    III = ("ИИИ", "Институт искусственного интеллекта")

    IKB = ("ИКБ", "Институт кибербезопасности и цифровых технологий")

    IPTIP = (
        "ИПТИП",
        "Институт перспективных технологий и индустриального программирования",
    )

    IRI = ("ИРИ", "Институт радиоэлектроники и информатики")

    ITU = ("ИТУ", "Институт технологий управления")

    ITHT = ("ИТХТ", "Институт тонких химических технологий им. М.В. Ломоносова")

    COLLEGE = ("КПК", "Колледж программирования и кибербезопасности")

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
    Enumeration of campuses.
    """

    __slots__ = ()

    MP_1 = ("МП-1", "ул. Малая Пироговская, д.1")
    V_78 = ("В-78", "Проспект Вернадского, д.78")
    V_86 = ("В-86", "Проспект Вернадского, д.86")
    S_20 = ("С-20", "ул. Стромынка, 20")
    SG_22 = ("СГ-22", "5-я ул. Соколиной горы, д.22")
    ONLINE = ("СДО", "СДО")
    BASE = ("База", "База")

    @staticmethod
    def get_by_name(name):
        for campus in Campus:
            if campus.name == name:
                return campus
        raise ValueError(f"Unknown campus name: {name}")

    @staticmethod
    def get_by_short_name(short_name):
        for campus in Campus:
            if campus.short_name == short_name:
                return campus
        raise ValueError(f"Unknown campus short name: {short_name}")

    @property
    def short_name(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]
