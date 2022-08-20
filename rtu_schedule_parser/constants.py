from enum import Enum, IntEnum


class LessonType(Enum):
    """Перечисление возможных типов занятий."""

    __slots__ = ()

    PRACTICE = "пр"
    LECTURE = "лек"
    INDIVIDUAL_WORK = "с/р"
    LABORATORY_WORK = "лаб"

    @staticmethod
    def get_by_name(lesson_type: str) -> "LessonType":
        """Получить тип занятия по строковому представлению."""
        if lesson_type == LessonType.PRACTICE.value:
            return LessonType.PRACTICE
        elif lesson_type == LessonType.LECTURE.value or lesson_type == "лк":
            return LessonType.LECTURE
        elif lesson_type == LessonType.INDIVIDUAL_WORK.value:
            return LessonType.INDIVIDUAL_WORK
        elif lesson_type == LessonType.LABORATORY_WORK.value:
            return LessonType.LABORATORY_WORK
        else:
            raise ValueError(f"Unknown lesson type: {lesson_type}")


class ScheduleDocumentType(IntEnum):
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
    def get_institute_by_name(name):
        for institute in Institute:
            if institute.name == name:
                return institute
        return None

    @staticmethod
    def get_institute_by_short_name(short_name):
        for institute in Institute:
            if institute.short_name == short_name:
                return institute
        return None


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
