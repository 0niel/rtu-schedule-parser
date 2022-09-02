from rtu_schedule_parser import ExcelScheduleParser
from rtu_schedule_parser.constants import Degree, Institute
from rtu_schedule_parser.downloader import ScheduleDownloader

if __name__ == "__main__":
    downloader = ScheduleDownloader()
    iit_docs = downloader.get_documents(
        specific_degrees={Degree.BACHELOR}, specific_institutes={Institute.IIT}
    )
    downloaded = downloader.download_all(iit_docs)
    print(downloaded)

    for doc in downloaded:
        schedule_data = ExcelScheduleParser(doc[1]).parse()
        print(schedule_data.get_groups())
