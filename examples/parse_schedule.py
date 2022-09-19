import os

from rtu_schedule_parser import ExcelScheduleParser, ScheduleData
from rtu_schedule_parser.downloader import ScheduleDownloader

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
    for doc, doc_path, is_downloaded in downloaded:
        print(f"Processing document: {doc}")

        parser = ExcelScheduleParser(doc_path, doc.period, doc.institute, doc.degree)
        if schedules is None:
            schedules = parser.parse(force=True)
        else:
            schedules.extend(parser.parse(force=True).get_schedule())

    # Initialize pandas dataframe
    df = schedules.get_dataframe()

    # groups count (unique)
    groups_count = df["group"].nunique()
    print(f"Groups count: {groups_count}")

    # get current script dir
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # save dataframe to csv
    df.to_csv(os.path.join(current_dir, "schedule.csv"))
    df.to_html(os.path.join(current_dir, "schedule.html"))
