def test_get_teacher_0(excel_formatter):
    result = excel_formatter.get_teachers("Козлова Г.Г.\nИсаев Р.А.")
    correct_result = ["Козлова Г.Г.", "Исаев Р.А."]
    assert result == correct_result


def test_get_teacher_1(excel_formatter):
    result = excel_formatter.get_teachers("Шеверева Е.А., Богатырев С.И.")
    correct_result = ["Шеверева Е.А.", "Богатырев С.И."]
    assert result == correct_result


def test_get_teacher_2(excel_formatter):
    result = excel_formatter.get_teachers(
        "Симонов М.А. Симонов М.А. Симонов М.А. Жлуткова"
    )
    correct_result = ["Симонов М.А.", "Симонов М.А.", "Симонов М.А.", "Жлуткова"]
    assert result == correct_result


def test_get_teacher_3(excel_formatter):
    result = excel_formatter.get_teachers("Симонов М.А. Жлуткова И.В.")
    correct_result = ["Симонов М.А.", "Жлуткова И.В."]
    assert result == correct_result


def test_get_teacher_4(excel_formatter):
    result = excel_formatter.get_teachers("Симонов М.А. . Жлуткова И.В.")
    correct_result = ["Симонов М.А.", "Жлуткова И.В."]
    assert result == correct_result


def test_get_teacher_5(excel_formatter):
    result = excel_formatter.get_teachers("Эйстрих-Геллер В.Ю.")
    correct_result = ["Эйстрих-Геллер В.Ю."]
    assert result == correct_result


def test_get_teacher_6(excel_formatter):
    result = excel_formatter.get_teachers("Рогачев")
    correct_result = ["Рогачев"]
    assert result == correct_result


def test_get_teacher_7(excel_formatter):
    result = excel_formatter.get_teachers("Рогачев Горелик")
    correct_result = ["Рогачев", "Горелик"]
    assert result == correct_result


def test_get_teacher_8(excel_formatter):
    result = excel_formatter.get_teachers("Новосёлова Е.В.")
    correct_result = ["Новосёлова Е.В."]
    assert result == correct_result


def test_get_teacher_9(excel_formatter):
    result = excel_formatter.get_teachers("Новосёлова Е.В.\nКомарова М,И.")
    correct_result = ["Новосёлова Е.В.", "Комарова М.И."]
    assert result == correct_result


def test_get_teacher_10(excel_formatter):
    result = excel_formatter.get_teachers("Беглов И.А., Верещагина Т.А.")
    correct_result = ["Беглов И.А.", "Верещагина Т.А."]
    assert result == correct_result


def test_get_teacher_11(excel_formatter):
    result = excel_formatter.get_teachers("123")
    assert result == []


def test_get_teacher_12(excel_formatter):
    result = excel_formatter.get_teachers("Ким Ю.Х, Ким Ю.Х., Ким Ю. Х., Ким Ю.Х")
    assert result == ["Ким Ю.Х.", "Ким Ю.Х.", "Ким Ю.Х.", "Ким Ю.Х."]


def test_get_teacher_13(excel_formatter):
    result = excel_formatter.get_teachers("Эйстрих-Геллер В.Ю, Эйстрих-Геллер В Ю.")
    assert result == ["Эйстрих-Геллер В.Ю.", "Эйстрих-Геллер В.Ю."]


def test_get_teacher_14(excel_formatter):
    result = excel_formatter.get_teachers("Казачкова О.А.,1 пг\nКазачкова О.А.,2 пг")
    assert result == [("Казачкова О.А.", 1), ("Казачкова О.А.", 2)]


def test_get_teacher_15(excel_formatter):
    result = excel_formatter.get_teachers("Мочалова Л.В.,Оранская И.А.")
    assert result == ["Мочалова Л.В.", "Оранская И.А."]


def test_get_teacher_16(excel_formatter):
    result = excel_formatter.get_teachers(
        "Скрипник С.В.,1 пг\n"
        "Скрипник С.В.,2 пг\n"
        "Мышечкин А.А.,1 пг\n"
        "Кудрявцев И.В.,2 пг\n"
        "Мышечкин А.А.,2 пг\n"
        "Кудрявцев И.В.,1 пг\n"
    )

    assert result == [
        ("Скрипник С.В.", 1),
        ("Скрипник С.В.", 2),
        ("Мышечкин А.А.", 1),
        ("Кудрявцев И.В.", 2),
        ("Мышечкин А.А.", 2),
        ("Кудрявцев И.В.", 1),
    ]


def test_get_teacher_17(excel_formatter):
    result = excel_formatter.get_teachers("Фиронов А.М.,1 п/г\n\nСадовникова Я.Э.")

    assert result == [
        ("Фиронов А.М.", 1),
        ("Садовникова Я.Э.", None),
    ]


def test_get_teacher_18(excel_formatter):
    result = excel_formatter.get_teachers("Десятсков А.В.,1 п/г\n\nСоловьев А.А.,2 п/г")

    assert result == [
        ("Десятсков А.В.", 1),
        ("Соловьев А.А.", 2),
    ]


def test_get_teacher_19(excel_formatter):
    result = excel_formatter.get_teachers(
        "Дальская Г.Ю.\n" "Рашутин Н.А.\n" "Юдин Г.А, 1 п/г\n" "Рашутин Н.А., 2 п/г"
    )

    assert result == [
        ("Дальская Г.Ю.", None),
        ("Рашутин Н.А.", None),
        ("Юдин Г.А.", 1),
        ("Рашутин Н.А.", 2),
    ]


def test_get_tacher_20(excel_formatter):
    result = excel_formatter.get_teachers("Амасев Д.В.,1 п/г\n\nЛобачев А.В.,2 п/г")

    assert result == [
        ("Амасев Д.В.", 1),
        ("Лобачев А.В.", 2),
    ]
