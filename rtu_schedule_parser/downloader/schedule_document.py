from rtu_schedule_parser.constants import Degree, Institute, ScheduleType
from rtu_schedule_parser.utils import academic_calendar


class ScheduleDocument:
    """ """

    institute: Institute
    schedule_type: ScheduleType
    degree: Degree
    period: academic_calendar.Period
    url: str

    def __init__(
        self,
        institute: Institute,
        schedule_type: ScheduleType,
        degree: Degree,
        period: academic_calendar.Period,
        url: str,
    ) -> None:
        self.institute = institute
        self.schedule_type = schedule_type
        self.degree = degree
        self.period = period
        self.url = url

    def __str__(self) -> str:
        return f"{self.institute} {self.schedule_type} {self.degree} {self.period} - [{self.url}]"

    def __repr__(self) -> str:
        return f"{self.institute} {self.schedule_type} {self.degree} {self.period} - [{self.url}]"
