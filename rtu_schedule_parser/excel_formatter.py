from __future__ import annotations

import re

from .constants import Campus, LessonType, RoomType
from .formatter import Formatter
from .schedule import Room


class ExcelFormatter(Formatter):
    """Реализация форматирования ячеек excel таблицы расписания к нужному формату."""

    # числа через запятую или тире
    _RE_NUMBERS = r"(?:\d+[-,\s.]*)+"

    # слова исключения недель
    _RE_EXCLUDE_WEEKS = r"\W*(?:кр|кроме)(?:\.|\b)"

    _RE_SUBGROUPS = r"(подгруппа|подгруп|подгр|п\/г|группа|гр)"

    # слова включения недель, игнорирование подгрупп
    _RE_WEEKS = rf"{_RE_NUMBERS}\s*(?:(?:нед|н)|\W)(?![.\s\d,-]*{_RE_SUBGROUPS})[.\s]*"

    # типы проводимого предмета
    _RE_LESSON_TYPES = r"(?:\b(лк|пр|лек|лаб)\b)"

    # ненужные символы в начале строки
    _RE_TRASH_START = r"(\A\W+\s*)"

    # ненужные символы в конце строки
    _RE_TRASH_END = r"([-,_.\+;]+$)"

    _RE_SEPARATORS = r" {2,}|\n|,|;"

    # Сокращённые название кампусов.
    CAMPUSES_SHORT_NAMES = {
        "МП-1": Campus.MP_1,
        "В-78": Campus.V_78,
        "В-86": Campus.V_86,
        "С-20": Campus.S_20,
        "СГ-22": Campus.SG_22,
    }

    # Сокращённые названия типов аудиторий.
    ROOM_TYPE_SHORT_NAMES = {
        "ауд": RoomType.AUDITORY,
        "лаб": RoomType.LABORATORY,
        "комп": RoomType.COMPUTERS,
        "физ": RoomType.SPORT,
    }

    def __format_subgroups_and_type(self, lesson: str) -> list:
        """Метод для форматирования сложных исключительных случаев в ячейке таблицы.

        Returns:
            list: список разделённых и отформатированных предметов
        """

        result = []

        # 2,4,6,8,10 (лк),12,14н (пр) Инструментарий информационно-аналитической деятельности
        # группа 1 - номера недель, группа 2 - тип предмета
        regexp_1 = r"(?:((?:\d+[-, \.]*)+(?:н|нед)?[. ]*)(?:[( ]*(лк|пр|лек|лаб)[) ]+))"

        # 1гр.= 2н.; 2гр.=4н. Криптографические методы защиты информации;
        # группа 1 - номер группы, группа 2 - номера недель
        regexp_2 = r"(?:(\d+[-, \.]*)+(?:группа|груп|гр|подгруппа|подгр)[. -]*=\s*((?:\d+[-, \.]*)+(?:нед|н)?[;. \b]+))"

        # 6,12н-1гр 4,10н-2 гр Материалы и технологии трехмерной печати в машиностр
        # группа 1 - номера недель, группа 2 - номер группы
        regexp_3 = r"(?:((?:\d+[-, \.]*)+(?:нед|н)[. ]*\-)(?:(\d+[-, =\.]*)+(?:группа|груп|гр|подгруппа|подгр)[. \b]*))"

        # (3,7,11,15 н. - лк; 5,9,13,17 н. - пр) Современные проблемы и методы прикладной информатики и развития
        # информационного общества
        # группа 1 - номера недель, группа 2 - тип предмета
        regexp_4 = (
            rf"({self._RE_NUMBERS}(?:н|нед)?[. ]*)(?:[- ]*(лк|пр|лек|лаб)(\b|[; ]+))"
        )

        expressions = [regexp_1, regexp_2, regexp_3, regexp_4]

        # Проверяем, какие из регулярных выражений выше подходит в нашем случае, затем разделяем предмет согласно
        # подгруппам, типам пары, неделям, удаляем мусор и возвращаем готовый список.
        for regexp in expressions:
            found = re.finditer(regexp, lesson)
            found_items = [x for x in found]
            if len(found_items) > 0:
                for week_types in found_items:
                    lesson = lesson.replace(week_types.group(), "")

                # удаление ненужных символов
                remove_trash = r"(\A\W+\s*)|([-,_\+;]+$)"
                lesson = re.sub(remove_trash, "", lesson)
                lesson = lesson.strip()
                list_lessons = lesson.split(";")

                group_substr = (
                    " подгруппа" if regexp == regexp_2 or regexp == regexp_3 else ""
                )

                if len(list_lessons) == 2 and len(found_items) == 4:
                    for i in range(len(found_items)):
                        index = int(i >= 2)

                        group_1 = re.sub(remove_trash, "", found_items[i].group(1))
                        group_1 = group_1.strip()

                        group_2 = re.sub(remove_trash, "", found_items[i].group(2))
                        group_2 = group_2.strip()

                        if regexp == regexp_2:
                            result.append(
                                f"{group_2} {list_lessons[index]} {group_1}{group_substr}"
                            )

                        else:
                            result.append(
                                f"{group_2} {list_lessons[index]} {group_2}{group_substr}"
                            )

                else:
                    for week_types in found_items:
                        group_1 = re.sub(remove_trash, "", week_types.group(1))
                        group_1 = group_1.strip()

                        group_2 = re.sub(remove_trash, "", week_types.group(2))
                        group_2 = group_2.strip()

                        if regexp == regexp_2:
                            result.append(f"{group_2} {lesson} {group_1}{group_substr}")
                        else:
                            result.append(f"{group_1} {lesson} {group_2}{group_substr}")

        return result

    def __split_lessons(self, lessons: str) -> list:
        """Разбивает строку с предметами на список названий предметов."""
        result = []

        # несколько предметов в одной ячейке и разделены
        # с помощью переноса строки.
        if "\n" in lessons:
            result = lessons.split("\n")
        # несколько предметов разделены большим количество пробелов.
        elif len(re.split(r" {3,}", lessons)) > 1:
            result = re.split(r" {3,}", lessons)

        # используем __format_subgroups_and_type, чтобы разделить
        # предметы по типу, если он указан, или по подгруппам, если они
        # указаны
        if len(result) > 0:
            for lesson in sorted(result):
                formatted_lessons = self.__format_subgroups_and_type(lesson)
                if len(formatted_lessons) > 0:
                    result.remove(lesson)
                    result += formatted_lessons

        else:
            formatted_lessons = self.__format_subgroups_and_type(lessons)
            if len(formatted_lessons) > 0:
                result += formatted_lessons

        # если len(result) == 0, то предыдущие методы форматирования не сработали,
        # а это скорее всего значит, что у нас один предмет, либо несколько
        # предметов записаны в одну строку
        if len(result) == 0:
            # пробуем разделить по ';'
            if ";" in lessons:
                result += lessons.split(";")
            else:
                # Обрабатываем случай, когда несколько предметов записаны
                # в одной строке, без разделителей (через пробел), либо это просто один предмет.
                # Пример нескольких предметов в одной строке:
                #
                # 1,3,9,13 Конфиденциальное делопроизводство 5,7,11,15 н. кр 5 н. Деньги, кредит,банки
                #
                # Регулярка для раделения дисциплин, написанных в одну строку. Захватывает номера недели, с помощью
                # позиций которых можно разделить предметы
                re_one_line_lessons = r"(?:\d+[-,\s.]*)+(?:(?:нед|н)|\b)[\. ]*(?:\(?(?:кроме|кр)? *(?:\d+[-,\s.]*)+(?:(?:нед|н)|\b)[\. ])(?![.\s,\-\d]*(?:подгруппа|подгруп|подгр|п\/г|группа|гр))"
                found = [x for x in re.finditer(re_one_line_lessons, lessons)]
                length = len(found)
                if length > 1:
                    for i in range(length):
                        current_found_pos = found[i].span()
                        is_last_element = i == length - 1
                        if is_last_element:
                            result.append(lessons[current_found_pos[0] :])
                        else:
                            next_found_pos = found[i + 1].span()
                            result.append(
                                lessons[current_found_pos[0] : next_found_pos[0]]
                            )
                else:
                    # одиночный предмет
                    result.append(lessons)

        return [lesson for lesson in result if lesson.strip() != ""]

    def __format_subgroups(self, lessons: list[str]) -> list[tuple[str, int | None]]:
        """Если подгруппа есть в строке, то возвращает подстроку без подгруппы и номер подгруппы."""
        re_subgroups = self._RE_NUMBERS + self._RE_SUBGROUPS
        new_lessons = []
        for i in range(len(lessons)):
            lesson = lessons[i]
            found = re.search(re_subgroups, lesson)
            if found:
                numbers_only = found.group(0).replace(found.group(1), "").strip()
                groups = self.__parse_numbers(numbers_only)
                if len(groups) == 1:
                    lesson = lesson.replace(found.group(0), "")
                    # На случай, если подгруппы указаны в скобках
                    lesson = re.sub(r"\(\W*\s*\)", "", lesson)
                    # удалить запятые в начале и конце строки
                    lesson = re.sub(r"^\s*,\s*|\s*,\s*$", "", lesson)
                    new_lessons.append((lesson, groups[0]))
                else:
                    new_lessons.append((lesson, None))
            else:
                new_lessons.append((lesson, None))
        return new_lessons

    def __parse_numbers(self, numbers_substr) -> list[int]:
        def parse_interval_numbers(substring: str):
            """Получение списка чисел из интервальной строки.
            Пример: 1-3 -> [1, 2, 3]
            """

            weeks_range = substring.split("-")
            return [
                week
                for week in range(
                    int(weeks_range[0].strip()), int(weeks_range[1].strip()) + 1
                )
            ]

        def parse_listed_numbers(substring: str):
            """Получение списка недель из строки с перечислением недель через
            запятую.
            Пример: 1,3,5 -> [1, 3, 5]
            """
            substring = re.sub(r"^([\W\s])+|([\W\s])+$", "", substring)
            weeks_list = substring.split(",")
            return [int(week.strip()) for week in weeks_list]

        numbers = []
        # интервальный способ задания + перечисление
        if "-" in numbers_substr and "," in numbers_substr:
            re_interval_numbers = r"(\d+ *- *\d+)"
            interval_weeks_substring = re.findall(re_interval_numbers, numbers_substr)[
                0
            ]

            numbers += parse_interval_numbers(interval_weeks_substring)
            weeks_substring = re.sub(re_interval_numbers, "", numbers_substr)
            # для удаления ненужных символов в начале и конце строки
            weeks_substring = re.sub(r"^([\W\s])+|([\W\s])+$", "", weeks_substring)
            numbers += parse_listed_numbers(weeks_substring)
            numbers.sort()

        # если это интервальный способ задания недель (прим.: 1-6 н.),
        # то создаём интервал из этих недель и не забываем проверить чётность
        elif "-" in numbers_substr:
            numbers += parse_interval_numbers(numbers_substr)

        # список недель через запятую
        elif "," in numbers_substr:
            numbers += parse_listed_numbers(numbers_substr)

        # если задана одиночная неделя
        else:
            clear_week = numbers_substr.strip()
            if len(clear_week) > 0:
                numbers.append(int(clear_week))
        return numbers

    def __fix_typos(self, names: str) -> str:
        """Исправление ошибок и опечаток в документе"""
        names = re.sub(r"деятельность\s*деятельность", "деятельность", names)
        names = re.sub(
            r"^\s*Военная\s*$", "Военная подготовка", names, flags=re.MULTILINE
        )
        names = re.sub(
            r"^\s*подготовка\s*$", "Военная подготовка", names, flags=re.MULTILINE
        )
        names = re.sub(r"^((\s*\d\s*п/г,*){2})$", "", names, flags=re.MULTILINE)
        # replace \n to space
        names = re.sub(r"(\n)(\d\s*п/г)", r" \g<2>", names, flags=re.MULTILINE)

        return names

    def __parse_weeks(
        self, weeks_substring: str, is_even: bool | None = None
    ) -> list[int]:
        """Получение недель из строки с учётом чётности."""
        weeks = self.__parse_numbers(weeks_substring)
        if is_even is not None:
            weeks = [week for week in weeks if week % 2 != is_even]
        return weeks

    def __get_only_lesson_name(self, lesson):
        """Возвращает только название предмета, удаляя лишнюю информацию (напр., номера недель)"""

        lesson = re.sub(self._RE_WEEKS, "", lesson)
        lesson = re.sub(self._RE_EXCLUDE_WEEKS, "", lesson)
        lesson = re.sub(self._RE_LESSON_TYPES, "", lesson)
        lesson = re.sub(self._RE_TRASH_START, "", lesson)
        lesson = re.sub(self._RE_TRASH_END, "", lesson)
        lesson = lesson.strip()

        return lesson

    def get_rooms(self, rooms_cell_value: str) -> list[Room]:
        result = []

        # Первая группа - тип аудитории, вторая - номер аудитории, третья - сокращенное название кампуса
        re_rooms = r"([а-яА-Я]+)\. ([а-яА-Я0-9-]+) \(([а-яА-Я0-9-]+)\)"
        rooms_list = re.findall(re_rooms, rooms_cell_value)
        for room in rooms_list:
            result.append(
                Room(
                    room[1],
                    self.CAMPUSES_SHORT_NAMES[room[2]],
                    self.ROOM_TYPE_SHORT_NAMES[room[0]],
                )
            )

        if result:
            return result

        for short_name in self.CAMPUSES_SHORT_NAMES:
            res = re.findall(short_name, rooms_cell_value, flags=re.A)
            if res:
                rooms = (
                    rooms_cell_value.replace("  ", "")
                    .replace("*", "")
                    .replace("\n", "")
                )
                rooms = re.sub(
                    res[0],
                    "",
                    rooms,
                    flags=re.A,
                )
                result.append(Room(rooms, self.CAMPUSES_SHORT_NAMES[short_name], None))
        if not result:
            rooms = re.split(r" {2,}|\n", rooms_cell_value)
            result = [Room(room, None, None) for room in rooms if room]
        return result

    def get_teachers(self, names_cell_value: str) -> list[str]:
        if not re.search(r"[а-яА-Я]", names_cell_value):
            return []

        teachers_names = names_cell_value.strip()

        re_typos = r"[а-яё]{1}(,) {0,2}[а-яё]{1}[. ]"
        typos = re.finditer(re_typos, teachers_names, flags=re.I)
        for typo in typos:
            teachers_names = (
                teachers_names[: typo.span(1)[0]]
                + "."
                + teachers_names[typo.span(1)[1] :]
            )

        # разделяем имена по разделителям
        names = re.split(self._RE_SEPARATORS, teachers_names)

        if len(names) > 1:
            result = [name.strip() for name in names if name.strip() != ""]
        else:
            # Имена с инициалами могут быть написаны в одной строке через пробелы.
            # Пример: Иванов И.И. Иванова И.И.
            re_teacher_name = r"(?:(?:(?:[а-яё\-]{1,}) +(?:[а-яё]{1}\. {0,2}){1,2})|(?:(?:[а-яё\-]{3,}) ?))"

            # поиск имён без учета регистра
            found = re.findall(re_teacher_name, teachers_names, flags=re.I)
            result = [x.strip() for x in found]

        return result

    def __get_lesson_by_name(self, name: str):
        """Получить тип занятия по строковому представлению."""
        if name == LessonType.PRACTICE.value or name == "п":
            return LessonType.PRACTICE
        elif (
            name == LessonType.LECTURE.value
            or name == "лк"
            or name == "лек"
            or name == "л"
        ):
            return LessonType.LECTURE
        elif name == LessonType.INDIVIDUAL_WORK.value or name == "ср":
            return LessonType.INDIVIDUAL_WORK
        elif name == LessonType.LABORATORY_WORK.value or name == "лб":
            return LessonType.LABORATORY_WORK
        else:
            raise ValueError(f"Unknown lesson type: {name}")

    def get_weeks(self, lesson: str, is_even=None, max_weeks=None) -> list[list[int]]:
        result = []

        lesson = self.__fix_typos(lesson)

        lessons = self.__split_lessons(lesson)

        for lesson in lessons:
            lesson = lesson.lower()

            include_weeks = (
                r"(\b(\d+[-, ]*)+)((н|нед)?(?![.\s,\-\d]*(?:подгруппа|подгруп|подгр|п\/г|группа|гр))"
                r"(\.|\b))"
            )
            exclude_weeks = r"(\b(кр|кроме)(\.|\b)\s*)" + include_weeks

            exclude_weeks_substr = re.search(exclude_weeks, lesson)
            # 4-я группа в данном контексте - это только номера недель.
            # см. https://regex101.com/
            exclude_weeks_substr = (
                "" if exclude_weeks_substr is None else exclude_weeks_substr.group(4)
            )

            # Необходимо исключить недели исключения из строки, чтобы недели
            # включения не пересекались с ними при вызове метода поиска
            lesson = re.sub(exclude_weeks, "", lesson)
            include_weeks_substr = re.search(include_weeks, lesson)
            include_weeks_substr = (
                "" if include_weeks_substr is None else include_weeks_substr.group(1)
            )

            # удаляем лишние пробелы слева и справа
            include_weeks_substr = include_weeks_substr.strip()
            exclude_weeks_substr = exclude_weeks_substr.strip()

            # получаем список int чисел неделю включения и исключения
            nums_include_weeks = self.__parse_weeks(include_weeks_substr, is_even)
            nums_exclude_weeks = self.__parse_weeks(exclude_weeks_substr, is_even)

            total_weeks = []

            # если не указаны недели включения, но указаны недели исключения, то это значит, что предмет проходит на
            # всех неделях, кроме недель исключений
            if len(nums_include_weeks) == 0 and len(nums_exclude_weeks) > 0:
                for i in range(1, max_weeks + 1):
                    if i not in nums_exclude_weeks:
                        if is_even is not None:
                            if bool(i % 2) != is_even:
                                total_weeks.append(i)
                        else:
                            total_weeks.append(i)
            elif len(nums_include_weeks) > 0:
                # Проверяем, недели предмета с помощью недель исключения
                for week in nums_include_weeks:
                    if week not in nums_exclude_weeks:
                        total_weeks.append(week)
            # Если список недель вообще не задан, т.е. предмет проходит всегда
            elif len(nums_include_weeks) == 0 and len(nums_exclude_weeks) == 0:
                if max_weeks is not None:
                    for i in range(1, max_weeks + 1):
                        if is_even is not None:
                            if bool(i % 2) != is_even:
                                total_weeks.append(i)
                        else:
                            total_weeks.append(i)
                else:
                    raise ValueError(
                        "No weeks specified for lesson. Please specify max_weeks parameter"
                    )

            result.append(total_weeks)

        return result

    def get_lessons(
        self, lessons_cell_value: str
    ) -> list[tuple[str, LessonType | None, int | None]]:
        lesson = self.__fix_typos(lessons_cell_value)

        lessons = self.__format_subgroups(self.__split_lessons(lesson))
        result = []

        for i in range(len(lessons)):
            types = re.findall(self._RE_LESSON_TYPES, lessons[i][0])

            if len(types) > 0:
                lesson_type = self.__get_lesson_by_name(types[0].lower().strip())
                result.append(
                    (
                        self.__get_only_lesson_name(lessons[i][0]),
                        lesson_type,
                        lessons[i][1],
                    )
                )
            else:
                result.append(
                    (self.__get_only_lesson_name(lessons[i][0]), None, lessons[i][1])
                )

        return [lesson for lesson in result if lesson[0].strip() != ""]

    def get_types(self, cell_value: str) -> list[LessonType]:
        types = re.split(self._RE_SEPARATORS, cell_value)

        return [
            self.__get_lesson_by_name(el.strip().lower()) for el in types if el != ""
        ]
