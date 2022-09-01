from rtu_schedule_parser.constants import LessonType


def test_formatter_1(excel_formatter):
    result = excel_formatter.get_types("лк\nлк")
    correct_result = [LessonType.LECTURE] * 2
    assert result == correct_result


def test_formatter_2(excel_formatter):
    result = excel_formatter.get_types("пр")
    correct_result = [LessonType.PRACTICE]
    assert result == correct_result


def test_formatter_3(excel_formatter):
    result = excel_formatter.get_types("лаб \nлаб")
    correct_result = [LessonType.LABORATORY_WORK, LessonType.LABORATORY_WORK]
    assert result == correct_result


def test_formatter_4(excel_formatter):
    result = excel_formatter.get_types("лк\nлк\nлк\nлк")
    correct_result = [LessonType.LECTURE] * 4
    assert result == correct_result
