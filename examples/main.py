import os

from rtu_schedule_parser import ExcelScheduleParser, ScheduleData
from rtu_schedule_parser.constants import Degree, Institute
from rtu_schedule_parser.downloader import ScheduleDownloader

if __name__ == "__main__":
    # Initialize downloader with default directory to save files
    downloader = ScheduleDownloader()
    # Get documents for specified institute and degree
    iit_docs = downloader.get_documents(
        specific_degrees={Degree.BACHELOR}, specific_institutes={Institute.IIT}
    )

    # Download only if they are not downloaded yet.
    downloaded = downloader.download_all(iit_docs)

    schedules = None  # type: ScheduleData | None
    for doc in downloaded:
        if schedules is None:
            schedules = ExcelScheduleParser(doc[1]).parse()
        else:
            schedules.extend(ExcelScheduleParser(doc[1]).parse().get_schedule())

    df = schedules.get_dataframe()
    # get only room, room_type and campus from dataframe
    df = df[["room", "room_type", "campus"]]
    # get unique values
    df = df.drop_duplicates()
    # sort by room name
    df = df.sort_values(by="room")
    # get current script dir
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # save dataframe to csv
    df.to_csv(os.path.join(current_dir, "rooms.csv"))
