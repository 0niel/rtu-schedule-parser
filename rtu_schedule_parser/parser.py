from abc import abstractmethod

from rtu_schedule_parser.formatter import Formatter


class ScheduleParser:
    def __init__(
        self, document_path: str, document_type: DocumentType, formatter: Formatter
    ) -> None:
        self._document_path = document_path
        self._document_type = document_type
        self._formatter = formatter

    @abstractmethod
    def parse(self):
        pass
