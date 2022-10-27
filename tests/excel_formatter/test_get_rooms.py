from rtu_schedule_parser.constants import Campus, RoomType
from rtu_schedule_parser.schedule import Room


def test_get_rooms_0(excel_formatter):
    result = excel_formatter.get_rooms("В-78*\nБ-105")
    correct_result = [Room("Б-105", Campus.V_78, None)]
    assert result == correct_result


def test_get_rooms_1(excel_formatter):
    result = excel_formatter.get_rooms("23452     Б-105")
    correct_result = [Room("23452", None, None), Room("Б-105", None, None)]
    assert result == correct_result


def test_get_rooms_2(excel_formatter):
    result = excel_formatter.get_rooms("В-78*А318 \n429")
    correct_result = [Room("А318 429", Campus.V_78, None)]
    assert result == correct_result


def test_get_rooms_3(excel_formatter):
    result = excel_formatter.get_rooms("И-304\nИ-306")
    correct_result = [Room("И-304", None, None), Room("И-306", None, None)]
    assert result == correct_result


def test_get_rooms_4(excel_formatter):
    result = excel_formatter.get_rooms("ИВЦ-107")
    correct_result = [Room("ИВЦ-107", None, None)]
    assert result == correct_result


def test_get_rooms_5(excel_formatter):
    result = excel_formatter.get_rooms("МП-1  \nА-301")
    correct_result = [Room("А-301", Campus.MP_1, None)]
    assert result == correct_result


def test_get_rooms_6(excel_formatter):
    result = excel_formatter.get_rooms("ауд. А-311 (В-78)")
    correct_result = [Room("А-311", Campus.V_78, RoomType.AUDITORY)]
    assert result == correct_result


def test_get_rooms_7(excel_formatter):
    result = excel_formatter.get_rooms("комп. И-204-а (В-78)")
    correct_result = [Room("И-204-а", Campus.V_78, RoomType.COMPUTERS)]
    assert result == correct_result


def test_get_rooms_8(excel_formatter):
    result = excel_formatter.get_rooms("физ. ФОК (В-78)")
    correct_result = [Room("ФОК", Campus.V_78, RoomType.SPORT)]
    assert result == correct_result


def test_get_rooms_9(excel_formatter):
    result = excel_formatter.get_rooms("ауд. Г-202 (В-78)\n\nлаб. М-110 (В-86)")
    correct_result = [
        Room("Г-202", Campus.V_78, RoomType.AUDITORY),
        Room("М-110", Campus.V_86, RoomType.LABORATORY),
    ]
    assert result == correct_result


def test_get_rooms_10(excel_formatter):
    result = excel_formatter.get_rooms("ауд. A-2 (В-78)")
    correct_result = [
        Room("А-2", Campus.V_78, RoomType.AUDITORY),
    ]
    assert result == correct_result


def test_get_rooms_11(excel_formatter):
    result = excel_formatter.get_rooms("ауд. А-140а (В-78)")
    correct_result = [
        Room("А-140-а", Campus.V_78, RoomType.AUDITORY),
    ]
    assert result == correct_result


def test_get_rooms_12(excel_formatter):
    result = excel_formatter.get_rooms("ауд. Г-101б (В-78)\n\nлаб. М-110в (В-86)")
    correct_result = [
        Room("Г-101-б", Campus.V_78, RoomType.AUDITORY),
        Room("М-110-в", Campus.V_86, RoomType.LABORATORY),
    ]
    assert result == correct_result

