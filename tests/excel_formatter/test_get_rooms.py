
from rtu_schedule_parser.constants import Campus


def test_get_rooms_0(excel_formatter):
    result = excel_formatter.get_rooms("В-78*\nБ-105")
    correct_result = [("Б-105", Campus.V_78)]
    assert result == correct_result


def test_get_rooms_1(excel_formatter):
    result = excel_formatter.get_rooms("23452     Б-105")
    correct_result = [("23452", None), ("Б-105", None)]
    assert result == correct_result


def test_get_rooms_2(excel_formatter):
    result = excel_formatter.get_rooms("В-78*А318 \n429")
    correct_result = [("А318 429", Campus.V_78)]
    assert result == correct_result


def test_get_rooms_3(excel_formatter):
    result = excel_formatter.get_rooms("И-304\nИ-306")
    correct_result = [("И-304", None), ("И-306", None)]
    assert result == correct_result


def test_get_rooms_4(excel_formatter):
    result = excel_formatter.get_rooms("ИВЦ-107")
    correct_result = [("ИВЦ-107", None)]
    assert result == correct_result


def test_get_rooms_5(excel_formatter):
    result = excel_formatter.get_rooms("МП-1  \nА-301")
    correct_result = [("А-301", Campus.MP_1)]
    assert result == correct_result
