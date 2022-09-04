from datetime import datetime

import rtu_schedule_parser.utils.academic_calendar as academic_calendar


def test_academic_calendar():
    date_now = datetime(2021, 9, 1)
    assert academic_calendar.get_period(date_now) == academic_calendar.Period(
        2021, 2022, 1
    )
    date_now_2 = datetime(2021, 1, 1)
    assert academic_calendar.get_period(date_now_2) == academic_calendar.Period(
        2020, 2021, 2
    )
    date_now_3 = datetime(2022, 9, 3)
    assert academic_calendar.get_period(date_now_3) == academic_calendar.Period(
        2022, 2023, 1
    )
