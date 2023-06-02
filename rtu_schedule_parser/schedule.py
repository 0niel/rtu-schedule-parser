from __future__ import annotations

import datetime
from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from rtu_schedule_parser.constants import (
    Campus,
    Degree,
    ExamType,
    Institute,
    LessonType,
    RoomType,
    TestSessionLessonType,
)
from rtu_schedule_parser.utils.academic_calendar import Month, Period, Weekday


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
    type: LessonType | TestSessionLessonType | None = None
    room: Room | None = None
    subgroup: int | None = None


@dataclass
class Exam:
    """
    Exam data class. Contains information about exam.
    """

    month: Month
    day: int
    name: str
    time_start: datetime.time
    teachers: list[str]
    rooms: list[Room]
    exam_type: ExamType


@dataclass
class ExamEmpty:
    """
    ExamEmpty data class. This is a cell in the schedule table that does not contain any information about the exam. It
    is used to fill the schedule table with empty cells.
    """

    month: Month
    day: int


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
class _Schedule(metaclass=ABCMeta):
    """
    For internal use only. Abstract class for schedule data. Contains information about the schedule of a group.
    """

    group: str
    period: Period
    institute: Institute
    degree: Degree

    document_url: Optional[str] = field(default_factory=lambda: None)

    _dataframe: pd.DataFrame | None = field(init=False, repr=False, default=None)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get pandas dataframe.
        """
        raise NotImplementedError(
            "Method is not implemented. Use `LessonsSchedule` or `ExamsSchedule` instead."
        )


@dataclass
class LessonsSchedule(_Schedule):
    """
    Schedule data class for lessons (semester schedule or test session schedule).
    """

    lessons: list[Lesson | LessonEmpty] = field(default_factory=lambda: [])

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


@dataclass
class ExamsSchedule(_Schedule):
    """
    Schedule data class for exams.
    """

    exams: list[Exam | ExamEmpty] = field(default_factory=lambda: [])

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get pandas dataframe. The dataframe contains the following columns: `group`, `month`, `day`,
        `exam`, `teachers`, `rooms`, `campus`, `room_type`, `exam_type`. If the dataframe has already been generated,
        then it will be returned from the cache. Otherwise, the dataframe will be generated and cached.
        """
        if self._dataframe is None:
            self._dataframe = self._generate_dataframe()

        return self._dataframe

    def _generate_dataframe(self):
        """
        Convert schedule to pandas dataframe. The dataframe contains the following columns: `group`, `month`, `day`,
        `exam`, `teachers`, `rooms`, `exam_type`, `time_start`.
        """
        df = pd.DataFrame(
            columns=[
                "group",
                "month",
                "day",
                "exam",
                "teachers",
                "rooms",
                "exam_type",
                "time_start",
            ]
        )

        for exam in self.exams:
            if type(exam) is not ExamEmpty:
                exam_rooms = ",".join(map(lambda room: room.name, exam.rooms))
                exam_teachers = ",".join(exam.teachers)
                df.loc[len(df)] = [
                    self.group,
                    exam.month,
                    exam.day,
                    exam.name,
                    exam_teachers,
                    exam_rooms,
                    "консультация"
                    if exam.exam_type == ExamType.CONSULTATION
                    else "экзамен",
                    exam.time_start,
                ]

        return df
