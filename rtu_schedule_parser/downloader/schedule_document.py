from dataclasses import dataclass

from rtu_schedule_parser.constants import Degree, Institute, ScheduleType
from rtu_schedule_parser.utils import academic_calendar


@dataclass(frozen=True)
class ScheduleDocument:
    """Class for storing information about schedule document."""

    institute: Institute
    schedule_type: ScheduleType
    degree: Degree
    period: academic_calendar.Period
    url: str
