import os
import re
import time

import bs4
import requests
from bs4 import BeautifulSoup

from rtu_schedule_parser.constants import Institute, ScheduleDocumentType

requests.adapters.DEFAULT_RETRIES = 5


SCHEDULE_URL = "https://www.mirea.ru/schedule/"

DEFAULT_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"

# Заголовки, под которыми хранятся соответствующие типы документов на странице с
# расписанием. Докуменов и этих заголовков может не быть, например, если ещё нет
# расписания для сессии.
SCHEDULE_TYPE_HEADERS = {
    ScheduleDocumentType.SEMESTER: "Расписание занятий",
    ScheduleDocumentType.TEST_SESSION: "Расписание зачетной сессии",
    ScheduleDocumentType.EXAM_SESSION: "Расписание экзаменационной сессии",
}


# Папки, в которых будут храниться документы с расписанием для указанных типов.
SCHEDULE_TYPE_FOLDERS = {
    ScheduleDocumentType.SEMESTER: "semester",
    ScheduleDocumentType.TEST_SESSION: "test_session",
    ScheduleDocumentType.EXAM_SESSION: "exam_session",
}


class ScheduleDownloader:
    """Класс используется для скачивания документов расписания с
    сайта РТУ МИРЭА

    Args:
    -------
        path_to_error_log (str, optional): путь и название файла
            для сохранения логов ошибок.
            По умолчанию = 'errors/downloader.log'.
        base_file_dir (str, optional): директория, в которую будут
            сохраняться скаченные документы расписания.
            По умолчанию = 'xls/'.
        except_types (list, optional): типы расписания, которые
            будут исключены. По умолчанию = [].
    """

    def __init__(
        self,
        base_file_dir="documents/",
        except_types=[],
    ):
        self._base_file_dir = base_file_dir
        self._file_types = ["xls", "xlsx", "pdf"]
        self._except_types = except_types
        self._download_dir = {
            "zach": [r"zach", r"zachety"],
            "exam": [r"zima", r"ekz", r"ekzam", r"ekzameny", r"sessiya"],
            "semester": [r""],
        }

    def __download_schedule(self, url: str, path: str):
        """Скачивание документа с расписанием (excel)

        Args:
        ----------
            url (str): Прямой URL до файла
            path (str): Путь с именем для сохраняемого файла

        Returns:
        ----------
            bool: True при успешном скачивании и False, если
                скачивание пропущено
        """
        # "_LATEST" будет означать, что расписание актуально
        # и заново парсить группы из этого документа не нужно
        actual_file_name = "_LATEST"

        file_path = None
        if os.path.isfile(path):
            file_path = path
        elif os.path.isfile(path + actual_file_name):
            file_path = path + actual_file_name

        if file_path:
            # сравнение двух файлов по их размеру
            # кажется, что это является ненадёжной штукой
            old_file_size = os.path.getsize(file_path)
            new_file_size = len(requests.get(url).content)

            if old_file_size != new_file_size:
                try:
                    # если появился более новый файл, то убираем '_LATEST',
                    # чтобы запустился парсинг групп
                    if actual_file_name in file_path:
                        file_path_to_rename = file_path
                        file_path = file_path.replace(actual_file_name, "")
                        os.rename(file_path_to_rename, file_path)
                    self.download_file(url, file_path=file_path)
                    return True
                except Exception as ex:
                    self._logger.error(f"Download failed with error: {ex}")
            else:
                if actual_file_name not in file_path:
                    os.rename(file_path, file_path + actual_file_name)
                return False

        try:
            self.download_file(url, file_path=path)
            return True
        except Exception as ex:
            self._logger.error(f"Download failed with error: {ex}")

    def __get_dir(self, file_name: str):
        """Возращает название папки, которая соответствует типу
        документа расписания

        Args:
        ----------
            file_name (str): Название файла расписания

        Returns:
        ----------
            str: Название директории
        """
        for dir_name in self._download_dir:
            for pattern in self._download_dir[dir_name]:
                if re.search(pattern, file_name, flags=re.IGNORECASE):
                    return dir_name

    def __parse_links_by_title(self, block_title: str, parse):
        """Получить список всех ссылок на документы из блоков
        расписания по заголовку. Например, если title == 'Расписание занятий:',
        то вернёт список всех ссылок на все документы с расписанием на семестр,
        проигнорируя расписание для сессии и др.

        Args:
            block_title (str): заголовок в блоке на сайте
            parse (BeautifulSoup): объект BS для парсинга
        """
        documents_links = []

        # мы ищем все заголовки в блоках с расписанием, это может быть
        # заголовок об экзаминационной сесии или т.п.
        schedule_titles = parse.find_all("b", class_="uk-h3")
        for title in schedule_titles:
            if title.text == block_title:
                # если это расписание занятий, то от носительно него
                # получаем главный блок, в котором находятся ссылки на
                # документы с расписанием
                all_divs = title.parent.parent.find_all("div", recursive=False)
                for i, div in enumerate(all_divs):
                    if block_title in div.text:
                        # проходимся по всем div'ам, начиная от блока
                        # с расписанием, заканчивая другим блоком с
                        # расписанием. Это нужно, т.к. эти блоки не
                        # имеют вложенности и довольно сложно определить
                        # где начинаются и кончаются документы с
                        # расписанием для семестра.
                        for j in range(i + 1, len(all_divs)):
                            # 'uk-h3' - класс заголовка расписания
                            if (
                                "uk-h3" not in str(all_divs[j])
                                and all_divs[j].text != block_title
                            ):
                                # поиск в HTML Всех классов с разметой Html
                                document = all_divs[j].find(
                                    "a", {"class": "uk-link-toggle"}
                                )
                                if document is not None:
                                    if document["href"] not in documents_links:
                                        documents_links.append(document["href"])
                            else:
                                break
        return documents_links

    def __download_college(self, html):
        parse_college = BeautifulSoup(html, "html.parser")
        document = parse_college.find("a", {"class": "uk-link-toggle"})
        if document is not None:
            url_file = document["href"]
            divided_path = os.path.split(url_file)
            file_name = divided_path[1]
            try:
                subdir = "college"
                path_to_file = os.path.join(self._base_file_dir, subdir, file_name)
                os.makedirs(os.path.join(self._base_file_dir, subdir), exist_ok=True)
                result = self.__download_schedule(url_file, path_to_file)

                if result:
                    self._logger.info("Download college: {0}".format(path_to_file))
                else:
                    self._logger.info("Skp college: {0}".format(path_to_file))

            except Exception as ex:
                self._logger.error(f"[{url_file}] message:" + str(ex))

    def __parse_institutes_cards(element: bs4.Tag) -> dict[Institute, bs4.Tag]:
        res = list()
        institutes_names = [institue.name() for institue in Institute]
        institues_cards = element.select("li > div > .uk-grid-margin > .uk-card-small")
        for card in institues_cards:
            for institutes_name in institutes_names:
                if institutes_name in card.get_text():
                    institute = Institute.get_institute_by_name(institutes_name)
                    res.append({institute: card})
                    break
        return res

    def download_file(self, url: str, file_path="", attempts=2):
        """Загружает содержимое URL-адреса в файл
        (с поддержкой больших файлов путем потоковой передачи)

        Args:
        ----------
            url (str): Прямой URL до файла
            file_path (str, optional): Путь с именем для сохраняемого
                файла. По умолчанию = ''.
            attempts (int, optional): Количество попыток скачивания
                одного файла. По умолчанию = 2.
        """
        for attempt in range(1, attempts + 1):
            try:
                if attempt > 1:
                    # 5 секунд ожидания между попытками скачивания
                    time.sleep(5)
                with requests.get(url, stream=True) as response:
                    # вызываем исключение в случае, если status_code
                    # будет неудовлетворительными
                    # (не находится в диапазоне 200-29)
                    response.raise_for_status()
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    return

            except Exception as ex:
                self._logger.error(
                    f"Download attempt #{attempt} ({url}) \
                    failed with error: {ex}"
                )

    def __download_files(self, file_links: list[str]):
        progress_all = len(file_links)

        # количество скачанных файлов
        count_file = 0

        for url_file in file_links:
            # получаем название файла из URL
            divided_path = os.path.split(url_file)
            file_name = divided_path[1]
            try:
                # название файла и его расширение
                (file_root, file_ext) = os.path.splitext(file_name)
                if (
                    file_ext.replace(".", "") in self._file_types
                    and "заоч" not in file_root
                ):
                    subdir = self.__get_dir(file_name)
                    path_to_file = os.path.join(self._base_file_dir, subdir, file_name)
                    if subdir not in self._except_types:
                        os.makedirs(
                            os.path.join(self._base_file_dir, subdir), exist_ok=True
                        )
                        result = self.__download_schedule(url_file, path_to_file)

                        count_file += 1
                        progress_percentage = count_file / len(progress_all) * 100

                        if result:
                            self._logger.info(
                                "Download : {0} -- {1}".format(
                                    path_to_file, progress_percentage
                                )
                            )
                        else:
                            self._logger.info(
                                "Skp : {0} -- {1}".format(
                                    path_to_file, progress_percentage
                                )
                            )
                    else:
                        continue
                else:
                    count_file += 1

            except Exception as ex:
                self._logger.error(f"[{url_file}] message:" + str(ex))

    def download(
        self,
        specific_documents_types: set[ScheduleDocumentType] = {},
        specific_institutes: set[Institute] = {},
    ) -> None:
        html = requests.get(SCHEDULE_URL).text
        bs4 = BeautifulSoup(html, "html.parser")
        # Вкладки расписания с кнопками для ступеней образования:
        # бакалавриат/специалитет, магистратура, аспирантура, колледж.
        # Наличие класса `uk-active` у элемента списка означает, данная вкладка
        # выбрана.
        schedule_tabs = bs4.find("div", {"id": "tabs"})  # type: bs4.Tag
        tabs_content = schedule_tabs.find("ul", {"id": "tab-content"})  # type: bs4.Tag

        # Вкладки:
        # БАКАЛАВРИАТ/СПЕЦИАЛИТЕТ, МАГИСТРАТУРА, АСПИРАНТУРА, КОЛЛЕДЖ, ЭКСТЕРНЫ
        tabs = tabs_content.find_all("li")[:4]  # первые 4 вкладки

        for i in range(len(tabs)):
            self.__parse_institutes_cards(tabs[i])

        # if specific_documents_types or specific_institutes:

        # if len(specific_institutes) != 0:
        #     for document_type in specific_documents_types:
        #         pass

        # for html in page_sources:
        #     # Объект BS с параметром парсера

        #     # списки адресов на файлы
        #     schedule_links = self.__parse_links_by_title("Расписание занятий:", parse)
        #     test_session_files = self.__parse_links_by_title(
        #         "Расписание зачетной сессии:", parse
        #     )

        #     self.__download_files(schedule_links)
        #     self.__download_files(test_session_files)

        # if college_page_source is not None:
        #     self.__download_college(college_page_source)
