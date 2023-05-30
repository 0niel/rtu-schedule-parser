import os
import concurrent.futures

from rtu_schedule_parser import ExcelScheduleParser, ScheduleData
from rtu_schedule_parser.constants import Degree, Institute, ScheduleType
from rtu_schedule_parser.downloader import ScheduleDownloader


def process_document(document_info):
    doc, doc_path, is_downloaded = document_info

    parser = ExcelScheduleParser(doc_path, doc.period, doc.institute, doc.degree)

    print(f"Processing document: {doc}")
    return parser.parse(force=True)


def download_docs():
    # Initialize downloader with default directory to save files
    downloader = ScheduleDownloader()

    # Get documents for specified institute and degree
    all_docs = downloader.get_documents(specific_schedule_types={ScheduleType.SEMESTER})

    # Download only if they are not downloaded yet.
    downloaded = downloader.download_all(all_docs)

    print(f"Downloaded {len(downloaded)} files")
    return downloaded

if __name__ == "__main__":
    # Download docs
    downloaded = download_docs()

    # Create schedule with downloaded files
    schedules = None  # type: ScheduleData | None

    # Create a ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_document, downloaded)

        for result in results:
            if schedules is None:
                schedules = result
            else:
                schedules.extend(result.get_schedule())

    schedules.generate_dataframe()

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