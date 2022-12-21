__version__ = "0.2.1"
__author__ = "Sergey Dmitriev"

from .excel_parser import ExcelScheduleParser
from .schedule import ExamsSchedule, Lesson, LessonEmpty, LessonsSchedule
from .schedule_data import ScheduleData
