import pandas as pd

from rtu_schedule_parser.schedule import LessonEmpty, Room, Schedule


class ScheduleData:
    def __init__(self, schedule: list[Schedule]):
        self._schedule = schedule
        self._df = self._generate_dataframe()

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
        self._schedule.append(schedule)
        self._df = self._generate_dataframe()

    def extend(self, schedule: list[Schedule]):
        self._schedule.extend(schedule)
        self._df = self._generate_dataframe()

    def get_schedule(self):
        return self._schedule

    def get_dataframe(self) -> pd.DataFrame:
        return self._df

    def get_rooms(self) -> list[Room]:
        rooms = []
        for schedule in self._schedule:
            for lesson in schedule.lessons:
                # if is not LessonEmpty type
                if type(lesson) is not LessonEmpty:
                    if lesson.room is not None and lesson.room not in rooms:
                        rooms.append(lesson.room)

        return rooms

    def get_group_schedule(self, group: str):
        for schedule in self._schedule:
            if schedule.group == group:
                return schedule

    def get_groups(self) -> list[str]:
        groups = []
        for schedule in self._schedule:
            if schedule.group not in groups:
                groups.append(schedule.group)

        return groups

    def get_degree(self):
        pass

    def get_course(self):
        pass

    def get_group_schedule(self, group: str):
        for schedule in self._schedule:
            if schedule.group == group:
                return schedule
        raise ValueError("Group not found")

    def get_units(self):
        pass

    def get_times(self):
        pass
