import pytest

from rtu_schedule_parser.formatter import Formatter


@pytest.fixture()
def excel_formatter() -> Formatter:
    from rtu_schedule_parser.excel_formatter import ExcelFormatter

    return ExcelFormatter()
