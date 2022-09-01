from __future__ import annotations

import datetime
import logging
import os

import bs4
import requests
from bs4 import BeautifulSoup

import rtu_schedule_parser.utils.academic_calendar as academic_calendar
from rtu_schedule_parser.constants import Degree, Institute, ScheduleType
from rtu_schedule_parser.downloader.schedule_document import ScheduleDocument

requests.adapters.DEFAULT_RETRIES = 5

logger = logging.getLogger(__name__)


class ScheduleDownloader:
    SCHEDULE_URL = "https://www.mirea.ru/schedule/"

    DEFAULT_USERAGENT = (
        "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
    )

    # Заголовки, под которыми хранятся соответствующие типы документов на странице с расписанием. Документов и этих
    # заголовков может не быть, например, если ещё нет расписания для сессии.
    SCHEDULE_TYPE_HEADERS = {
        ScheduleType.SEMESTER: "Расписание занятий",
        ScheduleType.TEST_SESSION: "Расписание зачетной сессии",
        ScheduleType.EXAM_SESSION: "Расписание экзаменационной сессии",
    }

    # Папки, в которых будут храниться документы с расписанием для указанных типов.
    SCHEDULE_TYPE_FOLDERS = {
        ScheduleType.SEMESTER: "semester",
        ScheduleType.TEST_SESSION: "test_session",
        ScheduleType.EXAM_SESSION: "exam_session",
    }

    ALLOWED_EXTENSIONS = [".pdf", ".xls", ".xlsx"]

    def __init__(
        self,
        base_file_dir="documents",
    ):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self._base_file_dir = os.path.join(current_path, base_file_dir)

    def __download_schedule(self, url: str, path: str) -> tuple[str, bool]:
        """
        Скачивание документа. Если файл уже существует, то он не будет перезаписан.

        Args:
            url: Ссылка на документ
            path: Путь, по которому будет сохранён документ

        Returns:
            Путь к сохранённому документу и флаг, был ли документ перезаписан.
        """

        if os.path.isfile(path):
            old_file = open(path, "rb").read()
            new_file = requests.get(url).content

            if old_file != new_file:
                try:
                    file_content = self.__request_file(url)
                    with open(path, "wb") as file:
                        file.write(file_content)
                    return path, True
                except Exception as ex:
                    logger.error(f"Download failed with error: {ex}")
            else:
                return path, False

        try:
            file_content = self.__request_file(url)
            with open(path, "wb") as file:
                file.write(file_content)
            return path, True
        except Exception as ex:
            logger.error(f"Download failed with error: {ex}")

    def __request_file(self, url: str) -> bytes:
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()

                return response.content

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Getting a file ({url}) failed with error: {http_err}")

    def __download_files(
        self, documents: list[ScheduleDocument]
    ) -> list[tuple[ScheduleDocument, str, bool]]:
        """
        Скачать множество документов.

        Args:
            documents: Список документов, которые нужно скачать.

        Returns: Список кортежей, в которых первый элемент - документ, второй - путь к скачанному файлу, третий - флаг,
        был ли файл перезаписан.
        """
        progress_all = len(documents)
        downloaded_files = 0

        res = list()

        for document in documents:
            url = document.url
            file_name = os.path.split(url)[1]
            try:
                # название файла и его расширение
                (file_root, file_ext) = os.path.splitext(file_name)

                if file_ext not in self.ALLOWED_EXTENSIONS:
                    continue

                subdir = self.SCHEDULE_TYPE_FOLDERS[document.schedule_type]
                file_dir = os.path.join(self._base_file_dir, subdir)

                os.makedirs(file_dir, exist_ok=True)

                path_to_file = os.path.join(file_dir, file_name)

                os.makedirs(os.path.join(self._base_file_dir, subdir), exist_ok=True)
                result = self.__download_schedule(url, path_to_file)
                res.append((document, result[0], result[1]))

                downloaded_files += 1
                progress_percentage = downloaded_files / progress_all * 100

                if result:
                    logger.info(
                        "Download : {0} -- {1}".format(
                            path_to_file, progress_percentage
                        )
                    )
                else:
                    logger.info(
                        "Skp : {0} -- {1}".format(path_to_file, progress_percentage)
                    )

            except Exception as ex:
                logger.error(f"[{url}] message:" + str(ex))

        return res

    def __parse_institute_cards(self, element: bs4.Tag) -> dict[Institute, bs4.Tag]:
        res = dict()
        institutes_names = [institute.name for institute in Institute]
        institutes_cards = element.select(
            "li > div > div > .uk-card.slider_ads.uk-card-body.uk-card-small > .uk-grid-small"
        )
        for card in institutes_cards:
            for institutes_name in institutes_names:
                if institutes_name in card.get_text():
                    institute = Institute.get_by_name(institutes_name)
                    res.update({institute: card})
                    break
        return res

    def __parse_links_by_type(
        self, document_types: ScheduleType, element: bs4.Tag
    ) -> list[str]:
        document_links = list()

        document_type_title = self.SCHEDULE_TYPE_HEADERS[document_types]
        schedule_titles = element.find_all("b", class_="uk-h3")
        for title in schedule_titles:
            if document_type_title in title.text:
                all_divs = title.parent.parent.find_all("div", recursive=False)
                for i, div in enumerate(all_divs):
                    if document_type_title in div.text:
                        # Проходим по всем div'ам, начиная от блока с расписанием, заканчивая другим блоком с
                        # расписанием. Это нужно, т.к. эти блоки не имеют вложенности и довольно сложно определить
                        # где начинаются и кончаются ссылки.
                        for j in range(i + 1, len(all_divs)):
                            # 'uk-h3' - класс заголовка расписания
                            if (
                                "uk-h3" not in str(all_divs[j])
                                and all_divs[j].text != document_type_title
                            ):
                                document = all_divs[j].find(
                                    "a", {"class": "uk-link-toggle"}
                                )
                                if document is not None:
                                    if document["href"] not in document_links:
                                        document_links.append(document["href"])
                            else:
                                break
        return document_links

    def download(self, schedule_document: ScheduleDocument) -> tuple[str, bool]:
        """
        Скачать документ.

        Args:
            schedule_document: Документ расписания.

        Returns: Кортеж, в котором первый элемент - путь к скачанному файлу, третий - флаг,
        был ли файл перезаписан.
        """
        try:
            file_name = os.path.split(schedule_document.url)[1]
            file_dir = os.path.join(
                self._base_file_dir,
                self.SCHEDULE_TYPE_FOLDERS[schedule_document.schedule_type],
            )
            os.makedirs(file_dir, exist_ok=True)
            return self.__download_schedule(
                schedule_document.url,
                os.path.join(
                    file_dir,
                    file_name,
                ),
            )
        except Exception as ex:
            logger.error(f"Download failed with error: {ex}")

    def download_all(
        self, schedule_documents: list[ScheduleDocument]
    ) -> list[tuple[ScheduleDocument, str, bool]]:
        """
        Скачать множество документов.

        Args:
            schedule_documents: Список документов расписания.

        Returns: Список кортежей, в котором первый элемент - документ, второй - путь к скачанному файлу, третий - флаг,
        был ли файл перезаписан.
        """
        return self.__download_files(schedule_documents)

    def get_documents(
        self,
        specific_schedule_types: set[ScheduleType] = None,
        specific_institutes: set[Institute] = None,
        specific_degrees: set[Degree] = None,
    ) -> list[ScheduleDocument]:
        """
        Получение информации о документах с расписанием с официального сайта.

        Args:
            specific_schedule_types: Если указано, то будут возвращены только документы с указанными типами.
            specific_institutes: Если указано, то будут возвращены только документы с расписанием указанных институтов.
            specific_degrees: Если указано, то будут возвращены только документы с расписанием указанных степеней.

        Returns:
            Список документов с расписанием.
        """

        if specific_schedule_types is None:
            specific_schedule_types = set()
        if specific_degrees is None:
            specific_degrees = set()
        if specific_institutes is None:
            specific_institutes = set()

        html = requests.get(self.SCHEDULE_URL).text
        bs = BeautifulSoup(html, "html.parser")
        # Вкладки расписания с кнопками для ступеней образования: бакалавриат/специалитет, магистратура, аспирантура,
        # колледж. Наличие класса `uk-active` у элемента списка означает, данная вкладка выбрана.
        schedule_tabs = bs.find("div", {"id": "tabs"})  # type: bs.Tag
        tabs_content = schedule_tabs.find("ul", {"id": "tab-content"})

        # Вкладки:
        # БАКАЛАВРИАТ/СПЕЦИАЛИТЕТ, МАГИСТРАТУРА, АСПИРАНТУРА, КОЛЛЕДЖ, ЭКСТЕРНЫ
        tabs_content = list(tabs_content.find_all("li"))[:4]  # первые 4 вкладки

        institute_schedule_cards = dict()  # type: dict[Degree, dict[Institute, bs.Tag]]

        for i in range(len(tabs_content)):
            if specific_degrees:
                if i + 1 not in [
                    specific_degree.value for specific_degree in specific_degrees
                ]:
                    continue

            degree = Degree(i + 1)
            institute_schedule_cards[degree] = self.__parse_institute_cards(
                tabs_content[i]
            )

        if specific_institutes:
            for degree in institute_schedule_cards:
                for institute in list(institute_schedule_cards[degree]):
                    if institute not in specific_institutes:
                        institute_schedule_cards[degree].pop(institute)

        if not specific_schedule_types:
            specific_schedule_types = set(ScheduleType)

        schedule_documents = list()

        for degree in institute_schedule_cards:
            for institute in institute_schedule_cards[degree]:
                for specific_document_type in specific_schedule_types:
                    links = self.__parse_links_by_type(
                        specific_document_type,
                        institute_schedule_cards[degree][institute],
                    )
                    for link in links:
                        schedule_documents.append(
                            ScheduleDocument(
                                institute,
                                specific_document_type,
                                degree,
                                academic_calendar.get_period(
                                    datetime.datetime.now().date()
                                ),
                                link,
                            )
                        )

        return schedule_documents
