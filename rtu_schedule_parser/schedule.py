from __future__ import annotations

import datetime
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from rtu_schedule_parser.constants import (
    Campus,
    Degree,
    Institute,
    LessonType,
    RoomType,
)
from rtu_schedule_parser.utils.academic_calendar import Period, Weekday


@dataclass(frozen=True)
class Room:
    """
    Room data class.
    """

    name: str = field()
    campus: Campus | None = field(default_factory=lambda: None)
    room_type: RoomType | None = field(default_factory=lambda: None)


@dataclass
class Lesson:
    """
    Lesson data class. Contains information about lesson. This class is used for lessons that are not empty. For
    empty lessons use `EmptyLesson` class.
    """

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


@dataclass(frozen=True)
class LessonEmpty:
    """
    Empty lesson. This is a cell in the schedule table that does not contain any information about the lesson. Used
    for filling schedule.
    """

    num: int
    weekday: Weekday
    time_start: datetime.time
    time_end: datetime.time


@dataclass
class Schedule:
    """
    Schedule data class. Contains information about the schedule of a group. The schedule is a list of lessons. Each
    lesson is a `Lesson` data class or `LessonEmpty` data class (if the cell in the schedule table is empty).
    """

    group: str
    lessons: list[Lesson | LessonEmpty]
    period: Period
    institute: Institute
    degree: Degree

    _dataframe: pd.DataFrame = field(init=False, repr=False, default=None)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get pandas dataframe. The dataframe contains the following columns: `group`, `lesson_num`,
        `lesson`, `weeks`, `weekday`, `teachers`, `time_start`, `time_end`, `type`, `room`, `campus`, `room_type`,
        `subgroup`. If the dataframe has already been generated, then it will be returned from the cache. Otherwise,
        the dataframe will be generated and cached.
        """
        if self._dataframe is None:
            self._dataframe = self._generate_dataframe()

        return self._dataframe

    def _generate_dataframe(self):
        """
        Convert schedule to pandas dataframe. The dataframe contains the following columns: `group`, `lesson_num`,
        `lesson`, `weeks`, `weekday`, `teachers`, `time_start`, `time_end`, `type`, `room`, `campus`, `room_type`,
        `subgroup`.
        """
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
                "room_type",
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
                lesson_room_type = (
                    lesson.room.room_type if lesson.room is not None else None
                )
                lesson_room_type = (
                    lesson_room_type.value if lesson_room_type is not None else np.nan
                )
                weeks = ",".join(str(week) for week in lesson.weeks)
                teachers = ",".join(lesson.teachers)
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
                    lesson_room_type,
                    lesson.subgroup or np.nan,
                ]

        return df
