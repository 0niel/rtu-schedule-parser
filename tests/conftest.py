import os

import pytest

from rtu_schedule_parser.downloader.schedule_downloader import ScheduleDownloader
from rtu_schedule_parser.formatter import Formatter


@pytest.fixture()
def excel_formatter() -> Formatter:
    from rtu_schedule_parser.excel_formatter import ExcelFormatter

    return ExcelFormatter()


@pytest.fixture()
def schedule_downloader() -> ScheduleDownloader:
    from rtu_schedule_parser.downloader import ScheduleDownloader

    # clear test folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(current_dir, "test")

    if os.path.exists(dir):
        # remove all files and dirs from folder
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.mkdir(dir)

    return ScheduleDownloader(base_file_dir=dir)
