import datetime
from dataclasses import dataclass
from enum import Enum

MAX_WEEKS = 17


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


@dataclass
class Period:
    year_start: int
    year_end: int
    semester: int


def get_period(date: datetime.date) -> Period:
    if date.month >= 7:
        return Period(date.year, date.year + 1, 1)
    else:
        return Period(date.year - 1, date.year, 2)
