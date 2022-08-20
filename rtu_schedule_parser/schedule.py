import datetime
from dataclasses import dataclass

from rtu_schedule_parser.constants import Campus, LessonType
from rtu_schedule_parser.utils.academic_calendar import Weekday


@dataclass
class Room:
    name: str
    campus: Campus | None = None


@dataclass
class Lesson:
    num: int
    name: str
    weeks: list[int]
    weekday: Weekday
    teachers: list[str]
    type: LessonType
    time_start: datetime.time
    time_end: datetime.time
    room: Room | None = None
    subgroup: int | None = None


@dataclass
class Schedule:
    group: str
    lessons: list[Lesson]
