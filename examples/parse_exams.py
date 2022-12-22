import os

from rtu_schedule_parser.constants import Degree, Institute
from rtu_schedule_parser.exams_excel_parser import ExcelExamScheduleParser
from rtu_schedule_parser.utils import Period

if __name__ == "__main__":

    doc_path = (os.path.join(os.path.dirname(__file__), "экз_ИИТ_2 курс_21-22_лето.xlsx"))

    parser = ExcelExamScheduleParser(
        doc_path, Period(2021, 2022, 2), Institute.IIT, Degree.BACHELOR
    )
    schedules = parser.parse(force=False, generate_dataframe=True)

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
