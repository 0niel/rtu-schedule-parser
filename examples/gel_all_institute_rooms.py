import os

from rtu_schedule_parser import ExcelScheduleParser, ScheduleData
from rtu_schedule_parser.downloader import ScheduleDownloader

if __name__ == "__main__":
    # Initialize downloader with default directory to save files
    downloader = ScheduleDownloader()
    # Get documents for specified institute and degree
    iit_docs = downloader.get_documents()

    # Download only if they are not downloaded yet.
    downloaded = downloader.download_all(iit_docs)
    print(f"Downloaded {len(downloaded)} files")

    # Create schedule with downloaded files
    schedules = None  # type: ScheduleData | None
    for doc, doc_path, is_downloaded in downloaded:
        print(f"Processing document: {doc}")
        try:
            parser = ExcelScheduleParser(
                doc_path,
                doc.period,
                doc.institute,
                doc.degree,
            )
            if schedules is None:
                schedules = parser.parse()
            else:
                schedules.extend(parser.parse().get_schedule())
        except Exception as e:
            print(f"Error while parsing {doc}: {e}")
    # Initialize pandas dataframe
    df = schedules.get_dataframe()
    # get only room, room_type and campus from dataframe
    df = df[["room", "room_type", "campus"]]
    # get unique values
    df = df.drop_duplicates()
    # sort by room name
    df = df.sort_values(by="room")
    # replace default dataframe index by length index
    df = df.reset_index(drop=True)
    # get current script dir
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # save dataframe to csv
    df.to_csv(os.path.join(current_dir, "rooms.csv"))
