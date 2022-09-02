# 2,4,6,16 н - пр/ 10,14 н - лр 1+2 гр
# Технологии и оборудование АП в машиностроении
# 8,12 н Защита интелл. собственности в машиностроении
from rtu_schedule_parser.constants import LessonType


# todo:
# 11,15 н/ 17 н Технологии обработки материалов концентрированными потоками энергии	[] лек/ лр


def test_get_lessons_0(excel_formatter):
    result = excel_formatter.get_lessons(
        "1-17 н. (кр. 3 н.) Архитектура утройств и систем вычислительной техники"
    )
    correct_result = [
        ("Архитектура утройств и систем вычислительной техники", None, None)
    ]
    assert result == correct_result


def test_get_lessons_1(excel_formatter):
    result = excel_formatter.get_lessons("кр. 3,5 н. Теория автоматического управления")
    correct_result = [("Теория автоматического управления", None, None)]
    assert result == correct_result


def test_get_lessons_2(excel_formatter):
    result = excel_formatter.get_lessons("8,10 н. Цифровые системы управления")
    correct_result = [("Цифровые системы управления", None, None)]
    assert result == correct_result


def test_get_lessons_3(excel_formatter):
    result = excel_formatter.get_lessons(
        "7 н. Вычислительные системы реального времени"
    )
    correct_result = [("Вычислительные системы реального времени", None, None)]
    assert result == correct_result


def test_get_lessons_4(excel_formatter):
    result = excel_formatter.get_lessons("2,6,10,14 н Экология\n4,8,12,16 Правоведение")
    correct_result = [("Экология", None, None), ("Правоведение", None, None)]
    assert result == correct_result


def test_get_lessons_5(excel_formatter):
    result = excel_formatter.get_lessons("Деньги, кредит, банки кр. 2,8,10 н.")
    correct_result = [("Деньги, кредит, банки", None, None)]
    assert result == correct_result


def test_get_lessons_6(excel_formatter):
    result = excel_formatter.get_lessons("2,6,10,14 н Экология\n4,8,12,16 Правоведение")
    correct_result = [
        ("Экология", None, None),
        ("Правоведение", None, None),
    ]
    assert result == correct_result


def test_get_lessons_7(excel_formatter):
    result = excel_formatter.get_lessons(
        "3,7,11,15  н Физика                                                     кр. 5,8,13.17 н Организация ЭВМ и Систем"
    )
    correct_result = [
        ("Физика", None, None),
        ("Организация ЭВМ и Систем", None, None),
    ]
    assert result == correct_result


def test_get_lessons_8(excel_formatter):
    result = excel_formatter.get_lessons(
        "Практика по получению профессиональных умений и опыта профессиональной деятельности"
    )
    correct_result = [
        (
            "Практика по получению профессиональных умений и опыта профессиональной деятельности",
            None,
            None,
        ),
    ]
    assert result == correct_result


def test_get_lessons_9(excel_formatter):
    result = excel_formatter.get_lessons(
        "4,8,12,16 н. Интерфейсы и периферийные устройства\n10 н. Микропроцессорные системы\n14 н. Микропроцессорные системы"
    )
    correct_result = [
        ("Интерфейсы и периферийные устройства", None, None),
        ("Микропроцессорные системы", None, None),
        ("Микропроцессорные системы", None, None),
    ]
    assert result == correct_result


def test_get_lessons_10(excel_formatter):
    result = excel_formatter.get_lessons(
        "кр.5 н. Основы научно-технического творчества"
    )
    correct_result = [
        ("Основы научно-технического творчества", None, None),
    ]
    assert result == correct_result


def test_get_lessons_11(excel_formatter):
    result = excel_formatter.get_lessons("Ин. яз")
    correct_result = [("Ин. яз", None, None)]
    assert result == correct_result


def test_get_lessons_12(excel_formatter):
    result = excel_formatter.get_lessons(
        "(3,7,11,15 н. - лк; 5,9,13,17 н. - пр) Современные проблемы и методы прикладной информатики и развития информационного общества"
    )
    correct_result = [
        (
            "Современные проблемы и методы прикладной информатики и развития информационного общества",
            LessonType.LECTURE,
            None,
        ),
        (
            "Современные проблемы и методы прикладной информатики и развития информационного общества",
            LessonType.PRACTICE,
            None,
        ),
    ]
    assert result == correct_result


def test_get_lessons_13(excel_formatter):
    result = excel_formatter.get_lessons("2-16 н. Разработка ПАОИАС")
    correct_result = [("Разработка ПАОИАС", None, None)]
    assert result == correct_result


def test_get_lessons_14(excel_formatter):
    result = excel_formatter.get_lessons("2,6,10,14нед. Техническая защита информации")
    correct_result = [("Техническая защита информации", None, None)]
    assert result == correct_result


def test_get_lessons_15(excel_formatter):
    result = excel_formatter.get_lessons(
        "кр. 5 н. Вычислительные системы реального времени"
    )
    correct_result = [("Вычислительные системы реального времени", None, None)]
    assert result == correct_result


def test_get_lessons_16(excel_formatter):
    result = excel_formatter.get_lessons(
        "7,9 н. Технические средства автоматизации и управления\n11,13,15 н. Теория автоматического управления"
    )
    correct_result = [
        ("Технические средства автоматизации и управления", None, None),
        ("Теория автоматического управления", None, None),
    ]

    assert result == correct_result


def test_get_lessons_17(excel_formatter):
    result = excel_formatter.get_lessons("Ин.яз. 1,2 подгр")
    correct_result = [("Ин.яз. 1,2 подгр", None, None)]
    assert result == correct_result


def test_get_lessons_18(excel_formatter):
    result = excel_formatter.get_lessons("……………………")
    correct_result = []
    assert result == correct_result


def test_get_lessons_19(excel_formatter):
    result = excel_formatter.get_lessons("Ознакомительная практика")
    correct_result = [("Ознакомительная практика", None, None)]
    assert result == correct_result


def test_get_lessons_21(excel_formatter):
    result = excel_formatter.get_lessons(
        "кр. 3,17 н. Организация работы с технотронными документами\n3 н. Организация работы с технотронными документами"
    )
    correct_result = [
        ("Организация работы с технотронными документами", None, None),
        ("Организация работы с технотронными документами", None, None),
    ]
    assert result == correct_result


def test_get_lessons_22(excel_formatter):
    result = excel_formatter.get_lessons(
        "11н Суд присяжных в России и зарубежных странах"
    )
    correct_result = [("Суд присяжных в России и зарубежных странах", None, None)]
    assert result == correct_result


def test_get_lessons_23(excel_formatter):
    result = excel_formatter.get_lessons("2,8, н Технологии развития имиджа территории")
    correct_result = [("Технологии развития имиджа территории", None, None)]
    assert result == correct_result


def test_get_lessons_24(excel_formatter):
    result = excel_formatter.get_lessons(
        "14н Основы конструирования и технологии приборостроения"
    )
    correct_result = [
        ("Основы конструирования и технологии приборостроения", None, None)
    ]
    assert result == correct_result


def test_get_lessons_25(excel_formatter):
    result = excel_formatter.get_lessons(
        "1,3,9,13 н. Конфиденциальное делопроизводство 5,7,11,15 н. Деньги, кредит,банки"
    )
    correct_result = [
        ("Конфиденциальное делопроизводство", None, None),
        ("Деньги, кредит,банки", None, None),
    ]
    assert result == correct_result


def test_get_lessons_26(excel_formatter):
    result = excel_formatter.get_lessons(
        "1,5,9,13 н. Физика (1 п/г)\n1,5,9,13 н. Физика (2 п/г)"
    )
    correct_result = [
        ("Физика", None, 1),
        ("Физика", None, 2),
    ]
    assert result == correct_result


def test_get_lessons_27(excel_formatter):
    result = excel_formatter.get_lessons("Ин.яз 1,2 подгруп")
    correct_result = [("Ин.яз 1,2 подгруп", None, None)]
    assert result == correct_result


def test_get_lessons_28(excel_formatter):
    result = excel_formatter.get_lessons("англ.яз. (2подгр.)")
    correct_result = [("англ.яз.", None, 2)]
    assert result == correct_result


def test_get_lessons_29(excel_formatter):
    result = excel_formatter.get_lessons(
        " 3,7,9 н Магнитодиагностика неоднородных материалов;  11,13,15 н Магнитодиагностика неоднородных материалов 1 гр; 17 н Магнитодиагностика неоднородных материалов 2 гр"
    )
    correct_result = [
        ("Магнитодиагностика неоднородных материалов", None, None),
        ("Магнитодиагностика неоднородных материалов", None, 1),
        ("Магнитодиагностика неоднородных материалов", None, 2),
    ]

    assert result == correct_result


def test_get_lessons_30(excel_formatter):
    result = excel_formatter.get_lessons(
        "1гр.=5,9,13н.; 2гр.=7,11,15н. Разработка и эксплуатация защищенных автоматизированных систем"
    )
    correct_result = [
        ("Разработка и эксплуатация защищенных автоматизированных систем", None, 1),
        ("Разработка и эксплуатация защищенных автоматизированных систем", None, 2),
    ]

    assert result == correct_result


def test_get_lessons_31(excel_formatter):
    result = excel_formatter.get_lessons(
        "5,7,11,13 н ФОПИ\n9 н Оптические аналитические приборы и методы исследований\n15 н Основы конструирования и технологии приборостроения"
    )
    correct_result = [
        ("ФОПИ", None, None),
        ("Оптические аналитические приборы и методы исследований", None, None),
        ("Основы конструирования и технологии приборостроения", None, None),
    ]

    assert result == correct_result


def test_get_lessons_32(excel_formatter):
    result = excel_formatter.get_lessons(
        "2-8 н Теория соединения материалов\n10,14н-1гр 12,16н-2 гр Тепл. проц. в ТС"
    )
    correct_result = [
        ("Теория соединения материалов", None, None),
        ("Тепл. проц. в ТС", None, 1),
        ("Тепл. проц. в ТС", None, 2),
    ]

    assert result == correct_result


def test_get_lessons_33(excel_formatter):
    result = excel_formatter.get_lessons(
        "2,4,6,8 н. Аудит 10,12 н. Финансовый мониторинг"
    )
    correct_result = [("Аудит", None, None), ("Финансовый мониторинг", None, None)]

    assert result == correct_result


def test_get_lessons_34(excel_formatter):
    result = excel_formatter.get_lessons(" 1,3,5,7 н Контроль и ревизия 9,11 Аудит")
    correct_result = [("Контроль и ревизия", None, None), ("Аудит", None, None)]
    assert result == correct_result


def test_get_lessons_35(excel_formatter):
    result = excel_formatter.get_lessons(
        "2,4,6,8 н Металловедение черных, цветных и драгоценных металлов и сплавов, 1 гр\n2,4,6,8  Методы неразрушающего контроля, 2 гр"
    )
    correct_result = [
        ("Металловедение черных, цветных и драгоценных металлов и сплавов", None, 1),
        ("Методы неразрушающего контроля", None, 2),
    ]
    assert result == correct_result


def test_get_lessons_36(excel_formatter):
    result = excel_formatter.get_lessons(
        "1гр.= 2н.; 2гр.=4н. Криптографические методы защиты информации;               6,8 н. Основы формирования каналов воздействия на информационные системы"
    )
    correct_result = [
        (
            "Основы формирования каналов воздействия на информационные системы",
            None,
            None,
        ),
        ("Криптографические методы защиты информации", None, 1),
        ("Криптографические методы защиты информации", None, 2),
    ]

    assert result == correct_result


def test_get_lessons_37(excel_formatter):
    result = excel_formatter.get_lessons(
        "2,4,6,8,10 (лк),12,14н (пр) Инструментарий информационно-аналитической деятельности\n2,4,6,8,10 н (пр) Практический аудит "
    )
    correct_result = [
        (
            "Инструментарий информационно-аналитической деятельности",
            LessonType.LECTURE,
            None,
        ),
        (
            "Инструментарий информационно-аналитической деятельности",
            LessonType.PRACTICE,
            None,
        ),
        ("Практический аудит", LessonType.PRACTICE, None),
    ]

    assert result == correct_result


def test_get_lessons_38(excel_formatter):
    result = excel_formatter.get_lessons(
        "1гр. 2,6,10,16 н. Безопасность систем баз данных\n8,12 н. Теория кодирования в системах защиты информации"
    )
    correct_result = [
        ("Безопасность систем баз данных", None, 1),
        ("Теория кодирования в системах защиты информации", None, None),
    ]
    assert result == correct_result


def test_get_lessons_39(excel_formatter):
    result = excel_formatter.get_lessons(
        "2гр. 2,6,10,16 н. Безопасность систем баз данных"
    )
    correct_result = [("Безопасность систем баз данных", None, 2)]
    assert result == correct_result


def test_get_lessons_40(excel_formatter):
    result = excel_formatter.get_lessons(
        "2-8 н Теория соединения материалов\n10,14н-1гр 12,16н-2 гр Тепл. проц. в ТС"
    )
    correct_result = [
        ("Теория соединения материалов", None, None),
        ("Тепл. проц. в ТС", None, 1),
        ("Тепл. проц. в ТС", None, 2),
    ]
    assert result == correct_result


def test_get_lessons_41(excel_formatter):
    result = excel_formatter.get_lessons(
        "1гр.=3,7,11,15; 2гр.=1,5,9,13н.Создание автоматизированных систем в защищенном исполнении"
    )
    correct_result = [
        ("Создание автоматизированных систем в защищенном исполнении", None, 1),
        ("Создание автоматизированных систем в защищенном исполнении", None, 2),
    ]
    assert result == correct_result


def test_get_lessons_42(excel_formatter):
    result = excel_formatter.get_lessons(
        "1гр.=4,8,12н.; 2гр.=6,10,14н. Разработка и эксплуатация защищенных автоматизированных систем; 1гр.=2,6,10,14н.; 2гр=4,8,12,16н.=Инфраструктура открытых ключей в СЗИ"
    )
    correct_result = [
        ("Разработка и эксплуатация защищенных автоматизированных систем", None, 1),
        ("Разработка и эксплуатация защищенных автоматизированных систем", None, 2),
        ("Инфраструктура открытых ключей в СЗИ", None, 1),
        ("Инфраструктура открытых ключей в СЗИ", None, 2),
    ]

    assert result == correct_result


def test_get_lessons_43(excel_formatter):
    result = excel_formatter.get_lessons(
        'кр. 5 н. Разработка конфигураций в среде "1С: Предприятие" '
    )
    correct_result = [('Разработка конфигураций в среде "1С: Предприятие"', None, None)]
    assert result == correct_result


def test_get_lessons_44(excel_formatter):
    result = excel_formatter.get_lessons(
        '10 н. Разработка конфигураций в среде "1С: Предприятие"  '
    )
    correct_result = [('Разработка конфигураций в среде "1С: Предприятие"', None, None)]
    assert result == correct_result


def test_get_lessons_45(excel_formatter):
    result = excel_formatter.get_lessons("История (история России, всеобщая история)")
    correct_result = [("История (история России, всеобщая история)", None, None)]
    assert result == correct_result


def test_get_lessons_46(excel_formatter):
    result = excel_formatter.get_lessons(
        "3,5 н. Введение в профессиональную деятельность \n7,9 н. Введение в профессиональную деятельность\n11,13 н. Введение в профессиональную деятельность деятельность\n15,17 н. Введение в профессиональную деятельность"
    )
    correct_result = [
        ("Введение в профессиональную деятельность", None, None) for i in range(4)
    ]
    assert result == correct_result


def test_get_lessons_47(excel_formatter):
    result = excel_formatter.get_lessons(
        "Технические методы диагностических исследований и лечебных воздействий\n"
        "2п/г,1п/г"
    )
    correct_result = [
        ("Технические методы диагностических исследований и лечебных воздействий", None, None)
    ]
    assert result == correct_result


def test_get_lessons_48(excel_formatter):
    result = excel_formatter.get_lessons(
        """3,7,11,15 н. Электротехника

5,9,13,17 н. Прикладная механика
"""
    )
    correct_result = [
        ("Электротехника", None, None),  ("Прикладная механика", None, None)
    ]
    assert result == correct_result


def test_get_lessons_49(excel_formatter):
    result = excel_formatter.get_lessons(
        "4,8,12,16 н. Электротехника\n2 п/г"
    )
    correct_result = [("Электротехника", None, 2)]
    assert result == correct_result

