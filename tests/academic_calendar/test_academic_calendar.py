from datetime import date, datetime

import rtu_schedule_parser.utils.academic_calendar as academic_calendar
from rtu_schedule_parser.utils.academic_calendar import Period


def test_academic_calendar():
    date_now = datetime(2021, 9, 1)
    assert academic_calendar.get_period(date_now) == Period(2021, 2022, 1)
    date_now_2 = datetime(2021, 1, 1)
    assert academic_calendar.get_period(date_now_2) == Period(2020, 2021, 2)
    date_now_3 = datetime(2022, 9, 3)
    assert academic_calendar.get_period(date_now_3) == Period(2022, 2023, 1)


def test_academic_calendar_2():
    assert academic_calendar.get_semester_start(Period(2020, 2021, 1)) == date(
        2020, 9, 1
    )
    assert academic_calendar.get_semester_start(Period(2020, 2021, 2)) == date(
        2021, 2, 9
    )

    assert academic_calendar.get_semester_start(Period(2021, 2022, 1)) == date(
        2021, 9, 1
    )
    assert academic_calendar.get_semester_start(Period(2021, 2022, 2)) == date(
        2022, 2, 9
    )

    assert academic_calendar.get_semester_start(Period(2022, 2023, 1)) == date(
        2022, 9, 1
    )
    assert academic_calendar.get_semester_start(Period(2022, 2023, 2)) == date(
        2023, 2, 9
    )

    assert academic_calendar.get_semester_start(Period(2023, 2024, 1)) == date(
        2023, 9, 1
    )
    assert academic_calendar.get_semester_start(Period(2023, 2024, 2)) == date(
        2024, 2, 9
    )

    assert academic_calendar.get_semester_start(Period(2024, 2025, 1)) == date(
        2024, 9, 2
    )
    assert academic_calendar.get_semester_start(Period(2024, 2025, 2)) == date(
        2025, 2, 10
    )

    assert academic_calendar.get_semester_start(Period(2025, 2026, 1)) == date(
        2025, 9, 1
    )
    assert academic_calendar.get_semester_start(Period(2025, 2026, 2)) == date(
        2026, 2, 9
    )
