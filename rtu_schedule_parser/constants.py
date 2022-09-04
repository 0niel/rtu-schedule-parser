from enum import Enum, IntEnum


class Degree(IntEnum):
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
    Enumeration of campuses.
    """

    __slots__ = ()

    MP_1 = "ул. Малая Пироговская, д.1"
    V_78 = "Проспект Вернадского, д.78"
    V_86 = "Проспект Вернадского, д.86"
    S_20 = "ул. Стромынка, 20"
    SG_22 = "5-я ул. Соколиной горы, д.22"
    ONLINE = "СДО"
