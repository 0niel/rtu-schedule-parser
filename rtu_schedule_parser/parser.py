from abc import ABCMeta, abstractmethod

from rtu_schedule_parser.constants import Degree, Institute
from rtu_schedule_parser.formatter import Formatter
from rtu_schedule_parser.schedule_data import ScheduleData
from rtu_schedule_parser.utils import Period


class ScheduleParser(metaclass=ABCMeta):
    """Abstract class for parsing schedule data."""

    def __init__(
        self,
        document_path: str,
        formatter: Formatter,
        course: int,
        period: Period,
        institute: Institute,
        degree: Degree,
    ) -> None:
        self._document_path = document_path
        self._formatter = formatter
        self._course = course
        self._period = period
        self._degree = degree
        self._institute = institute

    @abstractmethod
    def parse(self) -> ScheduleData:
        raise NotImplementedError
