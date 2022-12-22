__version__ = "2.0.0"
__author__ = "Sergey Dmitriev"

from .excel_parser import ExcelScheduleParser
from .schedule import ExamsSchedule,Exam, ExamEmpty, Lesson, LessonEmpty, LessonsSchedule
from .schedule_data import ScheduleData
