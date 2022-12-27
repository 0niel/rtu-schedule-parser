from __future__ import annotations

import pandas as pd

from rtu_schedule_parser.constants import ScheduleType
from rtu_schedule_parser.schedule import (
    ExamEmpty,
    ExamsSchedule,
    LessonEmpty,
    LessonsSchedule,
    Room,
)


class ScheduleData:
    """
    Schedule data for one institute. Contains list of schedules for each group.
    """

    def __init__(
        self,
        schedule: list[LessonsSchedule | ExamsSchedule],
        generate_dataframe: bool = False,
        schedule_type: ScheduleType = ScheduleType.SEMESTER,
    ):

        if not schedule:
            raise ValueError("Schedule cannot be empty")

        self.__current_type = (
            ExamsSchedule
            if schedule_type == ScheduleType.EXAM_SESSION
            else LessonsSchedule
        )

        # Test session format is equal to semester format
        if any(type(item) is not self.__current_type for item in schedule):
            raise TypeError(f"Schedule type must be {schedule_type}")

        self._schedule = schedule
        self._schedule_type = schedule_type
        self._df = None

        if generate_dataframe:
            self.generate_dataframe()

    def generate_dataframe(self) -> None:
        """
        Generate pandas dataframe.
        """
        df = None
        for schedule in self._schedule:
            dataframe = schedule.get_dataframe()
            # if df has no columns, add columns from dataframe
            df = dataframe if df is None else pd.concat([df, dataframe])

        df.index = range(len(df))

        self._df = df

    def append(self, schedule: LessonsSchedule | ExamsSchedule) -> None:
        """
        Append schedule to schedule data.
        """
        if type(schedule) is not self.__current_type:
            raise TypeError(f"Schedule type must be {self._schedule_type}")

        self._schedule.append(schedule)

        if self._df:
            self.generate_dataframe()

    def extend(self, schedule: list[LessonsSchedule | ExamsSchedule]):
        """
        Extend schedule data with another schedule data.
        """
        if any(type(item) is not self.__current_type for item in schedule):
            raise TypeError(f"Schedule type must be {self._schedule_type}")

        self._schedule.extend(schedule)
        if self._df is None or self._df.empty:
            self.generate_dataframe()

    def get_schedule(self) -> list[LessonsSchedule | ExamsSchedule]:
        """
        Get list of schedules.
        """
        return self._schedule

    def get_dataframe(self) -> pd.DataFrame | None:
        """
        Get pandas dataframe. If dataframe is not generated, return None. Use generate_dataframe() to generate
        dataframe.
        """
        if self._df is None or self._df.empty:
            raise ValueError(
                "Dataframe is not generated. Use generate_dataframe() to generate dataframe first."
            )

        return self._df

    def get_rooms(self) -> list[Room]:
        """
        Get list of all rooms. Rooms are unique.
        """
        rooms = []
        for schedule in self._schedule:
            if type(schedule) is LessonsSchedule:
                data = schedule.lessons
            else:
                data = schedule.exams

            for item in data:
                if (
                    type(item) is not LessonEmpty
                    and type(item) is not ExamEmpty
                    and item.room is not None
                    and item.room not in rooms
                ):
                    rooms.append(item.room)

        return rooms

    def get_group_schedule(self, group: str) -> LessonsSchedule | ExamsSchedule:
        """
        Get schedule for group.
        """
        for schedule in self._schedule:
            if schedule.group == group:
                return schedule

        raise ValueError("Group not found")

    def get_groups(self) -> list[str]:
        """
        Get list of all groups.
        """
        groups = []
        for schedule in self._schedule:
            if schedule.group not in groups:
                groups.append(schedule.group)

        return groups

    @property
    def schedule_type(self) -> ScheduleType:
        """
        Get schedule type. Schedule type is the same for all schedules in schedule data.
        """
        return self._schedule_type

    def __repr__(self) -> str:
        return f"ScheduleData({self._schedule}, {self._df}, {self._schedule_type})"

    # TODO:
    # def get_units(self):
    #     pass
    #
    # def get_times(self):
    #     pass
