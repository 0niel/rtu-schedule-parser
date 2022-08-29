import os
from rtu_schedule_parser.excel_parser import ExcelScheduleParser
from sqlalchemy import create_engine


engine = create_engine('sqlite:///C:/Users/foran/Desktop/schedules/schedule.db', echo=False)


if __name__ == "__main__":
    files_dir = "C:\\Users\\foran\\Desktop\\schedules"
    for filename in os.listdir(files_dir):
        parser = ExcelScheduleParser(os.path.join(files_dir, filename))
        schedule = parser.parse()
        df = schedule.get_dataframe()
        new_file_path = os.path.join(files_dir, filename.split(".")[0])
        df.to_csv(new_file_path + ".csv")
