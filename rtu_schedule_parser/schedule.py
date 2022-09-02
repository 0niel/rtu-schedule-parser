from __future__ import annotations

import datetime
from dataclasses import dataclass

import numpy as np
import pandas as pd

from rtu_schedule_parser.constants import Campus, LessonType, RoomType
from rtu_schedule_parser.utils.academic_calendar import Weekday


@dataclass
class Room:
    name: str
    campus: Campus | None = None
    room_type: RoomType | None = None


@dataclass
class Lesson:
    num: int
    name: str
    weeks: list[int]
    weekday: Weekday
    teachers: list[str]
    time_start: datetime.time
    time_end: datetime.time
    type: LessonType | None = None
    room: Room | None = None
    subgroup: int | None = None


@dataclass
class LessonEmpty:
    num: int
    weekday: Weekday
    time_start: datetime.time
    time_end: datetime.time


@dataclass
class Schedule:
    group: str
    lessons: list[Lesson | LessonEmpty]

    def to_dataframe(self):
        df = pd.DataFrame(
            columns=[
                "group",
                "lesson_num",
                "lesson",
                "weeks",
                "weekday",
                "teachers",
                "time_start",
                "time_end",
                "type",
                "room",
                "campus",
                "subgroup",
            ]
        )

        for lesson in self.lessons:
            if type(lesson) is not LessonEmpty:
                lesson_room = lesson.room.name if lesson.room is not None else np.nan
                lesson_campus = lesson.room.campus if lesson.room is not None else None
                lesson_campus = (
                    lesson_campus.value if lesson_campus is not None else np.nan
                )
                weeks = ",".join(str(week) for week in lesson.weeks)
                teachers = ",".join(teacher for teacher in lesson.teachers)
                lesson_type = lesson.type.value if lesson.type is not None else np.nan
                df.loc[len(df)] = [
                    self.group,
                    lesson.num,
                    lesson.name,
                    weeks,
                    lesson.weekday.value[1],
                    teachers,
                    lesson.time_start,
                    lesson.time_end,
                    lesson_type,
                    lesson_room,
                    lesson_campus,
                    lesson.subgroup if lesson.subgroup else np.nan,
                ]

        return df
