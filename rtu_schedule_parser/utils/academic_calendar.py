from enum import Enum


class Weekday(Enum):
    MONDAY = (1, "понедельник")
    TUESDAY = (2, "вторник")
    WEDNESDAY = (3, "среда")
    THURSDAY = (4, "четверг")
    FRIDAY = (5, "пятница")
    SATURDAY = (6, "суббота")
    SUNDAY = (7, "воскресенье")

    @staticmethod
    def get_weekday_by_number(number):
        for weekday in Weekday:
            if weekday.value[0] == number:
                return weekday
        raise ValueError("No weekday with number {}".format(number))

    @staticmethod
    def get_weekday_by_name(name):
        for weekday in Weekday:
            if weekday.value[1] == name:
                return weekday
        raise ValueError("No weekday with name {}".format(name))


class AcademicCalendar:
    MAX_WEEKS = 17

    MONTHS = {
        "январь": 1,
        "февраль": 2,
        "март": 3,
        "апрель": 4,
        "май": 5,
        "июнь": 6,
        "июлю": 7,
        "август": 8,
        "сентябрь": 9,
        "октябрь": 10,
        "ноябрь": 11,
        "декабрь": 12,
    }
