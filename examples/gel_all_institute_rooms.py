import os

import pandas as pd

from rtu_schedule_parser import ExcelScheduleParser, ScheduleData
from rtu_schedule_parser.constants import Institute
from rtu_schedule_parser.downloader import ScheduleDownloader

if __name__ == "__main__":
    # Initialize downloader with default directory to save files
    downloader = ScheduleDownloader()
    # Get documents for specified institute and degree
    iit_docs = downloader.get_documents(specific_institutes={Institute.IIT})

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

    rooms = schedules.get_rooms()
    print(f"Rooms count: {len(rooms)}")

    df = pd.DataFrame()

    for room in rooms:
        if room:
            room_name, room_type, room_campus = room.name, None, None
            if room.room_type:
                room_type = room.room_type.value
            if room.campus:
                room_campus = room.campus.value

            df = df.append(
                {
                    "room_name": room_name,
                    "room_type": room_type,
                    "room_campus": room_campus,
                },
                ignore_index=True,
            )

    df.reset_index(drop=True, inplace=True)

    # get current script dir
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # save dataframe to csv
    df.to_csv(os.path.join(current_dir, "rooms.csv"))
