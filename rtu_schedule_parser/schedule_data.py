import pandas as pd

from rtu_schedule_parser.schedule import LessonEmpty, Room, Schedule


class ScheduleData:
    """
    Schedule data for one institute. Contains list of schedules for each group.
    """

    def __init__(self, schedule: list[Schedule]):
        self._schedule = schedule
        self._df = self._generate_dataframe()

        institutes = set([schedule.institute for schedule in self._schedule])
        assert len(institutes) == 1, "Institutes must be the same"

    def _generate_dataframe(self):
        # Generate pandas dataframe from schedule
        df = None
        for schedule in self._schedule:
            dataframe = schedule.to_dataframe()
            # if df has no columns, add columns from dataframe
            if df is None:
                df = dataframe
            else:
                df = pd.concat([df, dataframe])

        df.index = range(len(df))

        return df

    def append(self, schedule: Schedule):
        """
        Append schedule to schedule data.
        """
        self._schedule.append(schedule)
        self._df = self._generate_dataframe()

    def extend(self, schedule: list[Schedule]):
        """
        Extend schedule data with another schedule data.
        """
        self._schedule.extend(schedule)
        self._df = self._generate_dataframe()

    def get_schedule(self) -> list[Schedule]:
        """
        Get list of schedules.
        """
        return self._schedule

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get pandas dataframe.
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
                if type(lesson) is not LessonEmpty:
                    if lesson.room is not None and lesson.room not in rooms:
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

    def get_units(self):
        pass

    def get_times(self):
        pass
