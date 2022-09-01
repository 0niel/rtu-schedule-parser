from abc import abstractmethod

from rtu_schedule_parser.formatter import Formatter
from rtu_schedule_parser.schedule_data import ScheduleData


class ScheduleParser:
    def __init__(self, document_path: str, formatter: Formatter) -> None:
        self._document_path = document_path
        self._formatter = formatter

    @abstractmethod
    def parse(self) -> ScheduleData:
        pass
