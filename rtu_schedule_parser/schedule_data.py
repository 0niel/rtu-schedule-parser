from __future__ import annotations

import pandas as pd

from rtu_schedule_parser.schedule import LessonEmpty, Room, Schedule


class ScheduleData:
    """
    Schedule data for one institute. Contains list of schedules for each group.
    """

    def __init__(self, schedule: list[Schedule], generate_dataframe: bool = False):
        self._schedule = schedule
        self._df = None

        if generate_dataframe:
            self._df = self.generate_dataframe()

    def generate_dataframe(self):
        """
        Generate pandas dataframe.
        """
        df = None
        for schedule in self._schedule:
            dataframe = schedule.get_dataframe()
            # if df has no columns, add columns from dataframe
            df = dataframe if df is None else pd.concat([df, dataframe])

        df.index = range(len(df))

        return df

    def append(self, schedule: Schedule):
        """
        Append schedule to schedule data.
        """
        self._schedule.append(schedule)
        self._df = self.generate_dataframe()

    def extend(self, schedule: list[Schedule]):
        """
        Extend schedule data with another schedule data.
        """
        self._schedule.extend(schedule)
        self._df = self.generate_dataframe()

    def get_schedule(self) -> list[Schedule]:
        """
        Get list of schedules.
        """
        return self._schedule

    def get_dataframe(self) -> pd.DataFrame | None:
        """
        Get pandas dataframe. If dataframe is not generated, return None. Use generate_dataframe() to generate
        dataframe.
        """
        return self._df

    def get_rooms(self) -> list[Room]:
        """
        Get list of all rooms. Rooms are unique.
        """
        rooms = []
        for schedule in self._schedule:
            for lesson in schedule.lessons:
                # if is not LessonEmpty type
                if (
                    type(lesson) is not LessonEmpty
                    and lesson.room is not None
                    and lesson.room not in rooms
                ):
                    rooms.append(lesson.room)

        return rooms

    def get_group_schedule(self, group: str) -> Schedule:
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

    # TODO:
    # def get_units(self):
    #     pass
    #
    # def get_times(self):
    #     pass
