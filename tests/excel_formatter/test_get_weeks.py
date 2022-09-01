def test_get_weeks_0(excel_formatter):
    result = excel_formatter.get_weeks(
        "кр. 3,17 н. Организация работы с технотронными документами\n3 н. Организация работы с технотронными документами",
        is_even=False,
        max_weeks=17,
    )
    correct_result = [[1, 5, 7, 9, 11, 13, 15], [3]]
    assert result == correct_result


def test_get_weeks_1(excel_formatter):
    result = excel_formatter.get_weeks(
        "1-17 н. (кр. 3 н.) Архитектура утройств и систем вычислительной техники"
    )
    correct_result = [[1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]
    assert result == correct_result


def test_get_weeks_2(excel_formatter):
    result = excel_formatter.get_weeks(
        "2,6,10,14 н Экология\n4,8,12,16 н. (кр. 4 нед) Правоведение"
    )
    correct_result = [[2, 6, 10, 14], [8, 12, 16]]
    assert result == correct_result


def test_get_weeks_3(excel_formatter):
    result = excel_formatter.get_weeks("Деньги, кредит, банки кр. 2,8,10 н.", True, 17)
    correct_result = [[4, 6, 12, 14, 16]]
    assert result == correct_result


def test_get_weeks_4(excel_formatter):
    result = excel_formatter.get_weeks("Орг. Химия (1-8 н.)")
    correct_result = [[1, 2, 3, 4, 5, 6, 7, 8]]
    assert result == correct_result


def test_get_weeks_5(excel_formatter):
    result = excel_formatter.get_weeks(
        "1,5,9,13 н Оперционные системы\n3,7,11,15 н  Оперционные системы", False
    )
    correct_result = [[1, 5, 9, 13], [3, 7, 11, 15]]
    assert result == correct_result


def test_get_weeks_6(excel_formatter):
    result = excel_formatter.get_weeks(
        "11н Суд присяжных в России и зарубежных странах"
    )
    correct_result = [[11]]
    assert result == correct_result


def test_get_weeks_7(excel_formatter):
    result = excel_formatter.get_weeks(
        "Система внешних и внутренних коммуникаций в организации лк/пр", None, 17
    )
    correct_result = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]
    assert result == correct_result


def test_get_weeks_8(excel_formatter):
    result = excel_formatter.get_weeks(
        "Система внешних и внутренних коммуникаций в организации лк/пр", False, 17
    )
    correct_result = [[1, 3, 5, 7, 9, 11, 13, 15, 17]]
    assert result == correct_result


def test_get_weeks_9(excel_formatter):
    result = excel_formatter.get_weeks(
        "1-11,15 н. предпринимательство и организация нового бизнеса"
    )
    correct_result = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15]]
    assert result == correct_result


def test_get_weeks_10(excel_formatter):
    result = excel_formatter.get_weeks(
        "1-11, 15, 16, 17 н. предпринимательство и организация нового бизнеса", True
    )
    correct_result = [[2, 4, 6, 8, 10, 16]]
    assert result == correct_result


def test_get_weeks_11(excel_formatter):
    result = excel_formatter.get_weeks(
        "1-11, 16 н. кр 5 н. предпринимательство и организация нового бизнеса",
        False,
    )
    correct_result = [[1, 3, 7, 9, 11]]
    assert result == correct_result


def test_get_weeks_12(excel_formatter):
    result = excel_formatter.get_weeks("2,8, н Технологии развития имиджа территории")
    correct_result = [[2, 8]]
    assert result == correct_result


def test_get_weeks_13(excel_formatter):
    result = excel_formatter.get_weeks(
        "14н Основы конструирования и технологии приборостроения"
    )
    correct_result = [[14]]
    assert result == correct_result


def test_get_weeks_14(excel_formatter):
    result = excel_formatter.get_weeks(
        "1,3,9,13 н. Конфиденциальное делопроизводство 5,7,11,15 н. Деньги, кредит,банки"
    )
    correct_result = [[1, 3, 9, 13], [5, 7, 11, 15]]
    assert result == correct_result


def test_get_weeks_15(excel_formatter):
    result = excel_formatter.get_weeks(
        "1,3,9,13 н. Конфиденциальное делопроизводство 5,7,11,15 н. кр 5 н. Деньги, кредит,банки"
    )
    correct_result = [[1, 3, 9, 13], [7, 11, 15]]
    assert result == correct_result


def test_get_weeks_16(excel_formatter):
    result = excel_formatter.get_weeks("1,3,5,7,9,11,13н Преддипломная практика")
    correct_result = [[1, 3, 5, 7, 9, 11, 13]]
    assert result == correct_result


def test_get_weeks_17(excel_formatter):
    result = excel_formatter.get_weeks(
        "1,5,9,13 н. Физика (1 п/г)\n1,5,9,13 н. Физика (2 п/г)"
    )
    correct_result = [[1, 5, 9, 13], [1, 5, 9, 13]]
    assert result == correct_result


def test_get_weeks_18(excel_formatter):
    result = excel_formatter.get_weeks("9,13,17 н. Физика\n9,13,17 н. Физика")
    correct_result = [[9, 13, 17], [9, 13, 17]]
    assert result == correct_result


def test_get_weeks_19(excel_formatter):
    result = excel_formatter.get_weeks(
        "1гр.=5,9,13н.; 2гр.=7,11,15н. Разработка и эксплуатация защищенных автоматизированных систем"
    )
    correct_result = [[5, 9, 13], [7, 11, 15]]
    assert result == correct_result


def test_get_weeks_20(excel_formatter):
    result = excel_formatter.get_weeks(
        "5,7,11,13 н ФОПИ\n9 н Оптические аналитические приборы и методы исследований\n15 н Основы конструирования и технологии приборостроения"
    )
    correct_result = [[5, 7, 11, 13], [9], [15]]
    assert result == correct_result


def test_get_weeks_21(excel_formatter):
    result = excel_formatter.get_weeks(
        "5,7,11,13 н ФОПИ\n9 н Оптические аналитические приборы и методы исследований\n15 н Основы конструирования и технологии приборостроения"
    )
    correct_result = [[5, 7, 11, 13], [9], [15]]
    assert result == correct_result


def test_get_weeks_22(excel_formatter):
    result = excel_formatter.get_weeks(
        "1гр. 2,6,10,16 н. Безопасность систем баз данных\n8,12 н. Теория кодирования в системах защиты информации"
    )
    correct_result = [[2, 6, 10, 16], [8, 12]]
    assert result == correct_result


def test_get_weeks_23(excel_formatter):
    result = excel_formatter.get_weeks(
        "2гр. 2,6,10,16 н. Безопасность систем баз данных"
    )
    correct_result = [[2, 6, 10, 16]]
    assert result == correct_result


def test_get_weeks_24(excel_formatter):
    result = excel_formatter.get_weeks("1,3,5,7 н. Контроль и ревизия 9,11 н. Аудит")
    correct_result = [[1, 3, 5, 7], [9, 11]]
    assert result == correct_result


def test_get_weeks_25(excel_formatter):
    result = excel_formatter.get_weeks("Ин.яз 1,2 подгруп", is_even=None, max_weeks=17)
    correct_result = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]
    assert result == correct_result


def test_get_weeks_26(excel_formatter):
    result = excel_formatter.get_weeks(
        "англ.яз. (2подгр.)", is_even=False, max_weeks=17
    )
    correct_result = [[1, 3, 5, 7, 9, 11, 13, 15, 17]]
    assert result == correct_result


def test_get_weeks_27(excel_formatter):
    result = excel_formatter.get_weeks(
        "1гр.= 2н.; 2гр.=4н. Криптографические методы защиты информации;               6,8 н. Основы формирования каналов воздействия на информационные системы"
    )
    correct_result = [[6, 8], [2], [4]]
    assert result == correct_result


def test_get_weeks_28(excel_formatter):
    result = excel_formatter.get_weeks(
        "2,4,6,8,10 (лк),12,14н (пр) Инструментарий информационно-аналитической деятельности\n2,4,6,8,10 н (пр) Практический аудит "
    )
    correct_result = [[2, 4, 6, 8, 10], [12, 14], [2, 4, 6, 8, 10]]
    assert result == correct_result


def test_get_weeks_29(excel_formatter):
    result = excel_formatter.get_weeks(
        "2-8 н Теория соединения материалов\n10,14н-1гр 12,16н-2 гр Тепл. проц. в ТС"
    )
    correct_result = [[2, 3, 4, 5, 6, 7, 8], [10, 14], [12, 16]]
    assert result == correct_result


def test_get_weeks_30(excel_formatter):
    result = excel_formatter.get_weeks(
        "1гр.=3,7,11,15; 2гр.=1,5,9,13н.Создание автоматизированных систем в защищенном исполнении"
    )
    correct_result = [[3, 7, 11, 15], [1, 5, 9, 13]]
    assert result == correct_result


def test_get_weeks_31(excel_formatter):
    result = excel_formatter.get_weeks(
        'кр. 5 н. Разработка конфигураций в среде "1С: Предприятие" ',
        is_even=False,
        max_weeks=17,
    )
    correct_result = [[1, 3, 7, 9, 11, 13, 15, 17]]
    assert result == correct_result


def test_get_weeks_32(excel_formatter):
    result = excel_formatter.get_weeks(
        '10 н. Разработка конфигураций в среде "1С: Предприятие"  '
    )
    correct_result = [[10]]
    assert result == correct_result


def test_get_weeks_33(excel_formatter):
    result = excel_formatter.get_weeks(
        "История (история России, всеобщая история)", is_even=None, max_weeks=17
    )
    correct_result = [[i for i in range(1, 18)]]
    assert result == correct_result


def test_get_weeks_34(excel_formatter):
    result = excel_formatter.get_weeks(
        "3,5 н. Введение в профессиональную деятельность \n7,9 н. Введение в профессиональную деятельность\n11,13 н. Введение в профессиональную деятельность деятельность\n15,17 н. Введение в профессиональную деятельность"
    )
    correct_result = [[3, 5], [7, 9], [11, 13], [15, 17]]
    assert result == correct_result


def test_get_weeks_35(excel_formatter):
    result = excel_formatter.get_weeks(
        """1,5,9,13 н. Речепреобразующие устройства

3,7,11,15 н. Речепреобразующие устройства
""",
        is_even=False,
        max_weeks=17,
    )
    correct_result = [[1, 5, 9, 13], [3, 7, 11, 15]]
    assert result == correct_result
