import datetime
from dataclasses import dataclass
from enum import Enum, IntEnum

import pytz

MAX_WEEKS = 17


class Month(IntEnum):
    """Month enum class"""

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    @classmethod
    def from_str(cls, value: str) -> "Month":
        """Returns the month enum value for the given month name."""
        return {
            "январь": cls.JANUARY,
            "февраль": cls.FEBRUARY,
            "март": cls.MARCH,
            "апрель": cls.APRIL,
            "май": cls.MAY,
            "июнь": cls.JUNE,
            "июль": cls.JULY,
            "август": cls.AUGUST,
            "сентябрь": cls.SEPTEMBER,
            "октябрь": cls.OCTOBER,
            "ноябрь": cls.NOVEMBER,
            "декабрь": cls.DECEMBER,
        }[value.lower()]


class Weekday(Enum):
    MONDAY = (1, "понедельник")
    TUESDAY = (2, "вторник")
    WEDNESDAY = (3, "среда")
    THURSDAY = (4, "четверг")
    FRIDAY = (5, "пятница")
    SATURDAY = (6, "суббота")
    SUNDAY = (7, "воскресенье")

    @staticmethod
    def get_weekday_by_number(number) -> "Weekday":
        for weekday in Weekday:
            if weekday.value[0] == number:
                return weekday
        raise ValueError(f"No weekday with number {number}")

    @staticmethod
    def get_weekday_by_name(name) -> "Weekday":
        for weekday in Weekday:
            if weekday.value[1] == name:
                return weekday
        raise ValueError(f"No weekday with name {name}")


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


def now_date() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone("Europe/Moscow"))


def get_week(date: datetime.datetime = None) -> int:
    """Возвращает номер учебной недели по дате
    Args:
        date (datetime.datetime, optional): Дата, для которой необходимо получить учебную неделю.
    """
    now = now_date() if date is None else date
    start_date = get_semester_start(date)

    if now.timestamp() < start_date.timestamp():
        return 1

    week = now.isocalendar()[1] - start_date.isocalendar()[1]

    if now.isocalendar()[2] != 0:
        week += 1

    return week


def get_day_by_week(period: Period, weekday: Weekday, week: int) -> datetime.date:
    """Returns the date of the day of the week by the week number
    Args:
        period: Period for which the date of the day of the week is required.
        weekday: Weekday for which the date of the day of the week is required.
        week: Week number for which the date of the day of the week is required.
    """
    start_date = get_semester_start(period)

    if week == 1:
        return start_date + datetime.timedelta(
            days=weekday.value[0] - 1 - start_date.weekday()
        )

    return start_date + datetime.timedelta(
        days=7 * (week - 1) + weekday.value[0] - 1 - start_date.weekday()
    )


def get_semester_start(period: Period) -> datetime.date:
    """Returns the start date of the semester by date
    Args:
        period: Period for which the start date of the semester is required.
    """

    if period.semester == 1:
        start_date = datetime.date(period.year_start, 9, 1)
        if start_date.weekday() == 6:
            start_date += datetime.timedelta(days=1)
        return start_date

    start_date = datetime.date(period.year_end, 2, 1)

    start_date += datetime.timedelta(days=8)

    if start_date.weekday() == 6:
        start_date += datetime.timedelta(days=1)

    return start_date
