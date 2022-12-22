__version__ = "2.0.0"
__author__ = "Sergey Dmitriev"

from .excel_parser import ExcelScheduleParser
from .schedule import (
    Exam,
    ExamEmpty,
    ExamsSchedule,
    Lesson,
    LessonEmpty,
    LessonsSchedule,
)
from .schedule_data import ScheduleData
