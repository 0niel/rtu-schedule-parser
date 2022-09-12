import os
import pandas as pd
import datetime

from rtu_schedule_parser import ExcelScheduleParser, ScheduleData, LessonEmpty
from rtu_schedule_parser.downloader import ScheduleDownloader
from rtu_schedule_parser.excel_formatter import ExcelFormatter


def calculate_day_by_week(week: int, weekday: int) -> datetime.date:
    """Calculate day number by week and weekday."""
    start_date = datetime.date(2022, 8, 29)
    delta = datetime.timedelta(days=7 * (week - 1) + weekday - 1)
    return start_date + delta


if __name__ == "__main__":
    # Initialize downloader with default directory to save files
    downloader = ScheduleDownloader()
    # Get documents for specified institute and degree
    all_docs = downloader.get_documents()

    # Download only if they are not downloaded yet.
    downloaded = downloader.download_all(all_docs)

    print(f"Downloaded {len(downloaded)} files")

    # Create schedule with downloaded files
    schedules = None  # type: ScheduleData | None
    for doc in downloaded:
        print(f"Processing document: {doc}")

        parser = ExcelScheduleParser(
            doc[1], doc[0].period, doc[0].institute, doc[0].degree
        )
        if schedules is None:
            schedules = parser.parse(force=True)
        else:
            schedules.extend(parser.parse(force=True).get_schedule())

    # Invert `ExcelFormatter.CAMPUSES_SHORT_NAMES`. It is needed to get campus short name by campus.
    campuses = {v: k for k, v in ExcelFormatter.CAMPUSES_SHORT_NAMES.items()}

    for schedule in schedules.get_schedule():
        # Subject (Пример: Математический анализ),
        # Start Date (Пример: 05/30/2020)
        # Start Time (Пример: 10:00 AM)
        # End Date (Пример: 05/30/2020)
        # End Time (Пример: 1:00 PM)
        # Description (Иванов И.И.)
        # Location (Пример: "А-420 (В-78)")
        google_calendar_df = pd.DataFrame()

        for lesson in schedule.lessons:
            if type(lesson) is not LessonEmpty:
                for week in lesson.weeks:
                    lesson_type = ''
                    if lesson_type:
                        lesson_type = f' ({lesson.type.value})'
                    subject = f"{lesson.num} | {lesson.name}{lesson_type}"
                    start_time = lesson.time_start.strftime("%I:%M %p")
                    end_time = lesson.time_end.strftime("%I:%M %p")
                    start_date = calculate_day_by_week(week, lesson.weekday.value[0])
                    if start_date.month < 9:
                        continue
                    end_date = start_date
                    description = ', '.join(lesson.teachers)
                    location = lesson.room.name if lesson.room else ''
                    if lesson.room:
                        if lesson.room.campus:
                            location = f"{location} ({campuses[lesson.room.campus]})"

                    row = {
                        "Subject": subject,
                        "Start Date": start_date,
                        "Start Time": start_time,
                        "End Date": end_date,
                        "End Time": end_time,
                        "Description": description,
                        "Location": location
                    }

                    google_calendar_df = google_calendar_df.append(row, ignore_index=True)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        # create output dir
        output_dir = os.path.join(current_dir, "output")
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # save dataframe to csv
        google_calendar_df.to_csv(os.path.join(output_dir, f"{schedule.group}.csv"))
