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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ScheduleDownloader:
    # Link to the schedule page.
    SCHEDULE_URL = "https://www.mirea.ru/schedule/"

    # Folder names for each schedule type.
    SCHEDULE_TYPE_FOLDERS = {
        ScheduleType.SEMESTER: "semester",
        ScheduleType.TEST_SESSION: "test_session",
        ScheduleType.EXAM_SESSION: "exam_session",
    }

    _DEFAULT_USERAGENT = (
        "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
    )

    # Schedule type headers are located in the <h3> tag. These are the headers under which the corresponding types of
    # documents are stored on the schedule page. Documents and these headers may not exist, for example, if there is
    # no schedule for the session yet.
    _SCHEDULE_TYPE_HEADERS = {
        ScheduleType.SEMESTER: "Расписание занятий",
        ScheduleType.TEST_SESSION: "Расписание зачетной сессии",
        ScheduleType.EXAM_SESSION: "Расписание экзаменационной сессии",
    }

    # Allowed file extensions to download.
    _ALLOWED_EXTENSIONS = [".pdf", ".xls", ".xlsx"]

    def __init__(
        self,
        base_file_dir="documents",
    ):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self._base_file_dir = os.path.join(current_path, base_file_dir)

    def __download_schedule(self, url: str, path: str) -> tuple[str, bool]:
        """
        Download schedule from the specified url. If the file already exists, it will be not overwritten.

        Args:
            url: Url to download the file from.
            path: Path to the file to download.

        Returns:
            Tuple with path to downloaded file and flag, that indicates whether file was overwritten or first
            time downloaded.
        """

        if os.path.isfile(path):
            old_file = open(path, "rb").read()
            new_file = requests.get(url).content

            if old_file == new_file:
                return path, False

            try:
                return self.__extracted_from___download_schedule_20(url, path)
            except Exception as ex:
                logger.error(f"Download failed with error: {ex}")
        try:
            return self.__extracted_from___download_schedule_20(url, path)
        except Exception as ex:
            logger.error(f"Download failed with error: {ex}")

    # TODO Rename this here and in `__download_schedule`
    def __extracted_from___download_schedule_20(self, url, path):
        file_content = self.__request_file(url)
        with open(path, "wb") as file:
            file.write(file_content)
        return path, True

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
        Download files from the list of documents.

        Args:
            documents: List of documents to download.

        Returns: List of tuples with downloaded document, path to the downloaded file and flag, whether the file was
            overwritten/first downloaded or not.
        """
        progress_all = len(documents)
        downloaded_files = 0

        res = []

        for document in documents:
            url = document.url
            file_name = os.path.split(url)[1]
            try:
                # название файла и его расширение
                (file_root, file_ext) = os.path.splitext(file_name)

                if file_ext not in self._ALLOWED_EXTENSIONS:
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
                logger.error(f"[{url}] message:{str(ex)}")

        return res

    def __parse_institute_cards(self, element: bs4.Tag) -> dict[Institute, bs4.Tag]:
        res = {}
        institutes_names = [institute.name for institute in Institute]
        institutes_cards = element.select(
            "li > div > div > .uk-card.slider_ads.uk-card-body.uk-card-small > .uk-grid-small"
        )
        for card in institutes_cards:
            for institutes_name in institutes_names:
                if institutes_name in card.get_text():
                    institute = Institute.get_by_name(institutes_name)
                    res[institute] = card
                    break
        return res

    def __parse_links_by_type(
        self, document_types: ScheduleType, element: bs4.Tag
    ) -> list[str]:
        document_links = []

        document_type_title = self._SCHEDULE_TYPE_HEADERS[document_types]
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
                            if (
                                "uk-h3" in str(all_divs[j])
                                or all_divs[j].text == document_type_title
                            ):
                                break
                            document = all_divs[j].find(
                                "a", {"class": "uk-link-toggle"}
                            )
                            if (
                                document is not None
                                and document["href"] not in document_links
                            ):
                                document_links.append(document["href"])
        return document_links

    def download(self, schedule_document: ScheduleDocument) -> tuple[str, bool]:
        """
        Download a schedule document.

        Args:
            schedule_document: Schedule document to download.

        Returns:
            Tuple with path to downloaded file and flag, that indicates whether file was overwritten or first
            time downloaded.
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
        Download many documents.

        Args:
            schedule_documents: List of documents.

        Returns:
            List of tuples, where first element is document, second is path to file, third is flag,
            was file overwritten or first time downloaded.
        """
        return self.__download_files(schedule_documents)

    def get_documents(
        self,
        specific_schedule_types: set[ScheduleType] = None,
        specific_institutes: set[Institute] = None,
        specific_degrees: set[Degree] = None,
    ) -> list[ScheduleDocument]:
        """
        Get all documents from site. If specific_schedule_types, specific_institutes or specific_degrees is not None,
        then return only documents with specific types, institutes or degrees.

        Args:
            specific_schedule_types: Specific schedule types. If None, then return all documents. Default is None.
            specific_institutes: Specific institutes. If None, then return all documents. Default is None.
            specific_degrees: Specific degrees. If None, then return all documents. Default is None.

        Returns:
            List of documents.
        """

        if specific_schedule_types is None:
            specific_schedule_types = set()
        if specific_degrees is None:
            specific_degrees = set()
        if specific_institutes is None:
            specific_institutes = set()

        html = requests.get(self.SCHEDULE_URL).text
        bs = BeautifulSoup(html, "html.parser")

        # Schedule tabs with education levels: bachelor, master, etc. The presence of the `uk-active` class in the
        # list item means that this tab is selected.
        schedule_tabs = bs.find("div", {"id": "tabs"})  # type: bs.Tag
        tabs_content = schedule_tabs.find("ul", {"id": "tab-content"})

        # Tabs:
        # "БАКАЛАВРИАТ/СПЕЦИАЛИТЕТ", "МАГИСТРАТУРА", "АСПИРАНТУРА", "КОЛЛЕДЖ", "ЭКСТЕРНЫ"
        tabs_content = list(tabs_content.find_all("li"))[:4]  # first 4 tabs

        institute_schedule_cards = {}

        for i in range(len(tabs_content)):
            if specific_degrees and i + 1 not in [
                specific_degree.value for specific_degree in specific_degrees
            ]:
                continue

            degree = Degree(i + 1)
            institute_schedule_cards[degree] = self.__parse_institute_cards(
                tabs_content[i]
            )

        if specific_institutes:
            for degree, value in institute_schedule_cards.items():
                for institute in list(value):
                    if institute not in specific_institutes:
                        institute_schedule_cards[degree].pop(institute)

        if not specific_schedule_types:
            specific_schedule_types = set(ScheduleType)

        schedule_documents = []

        for degree, value_ in institute_schedule_cards.items():
            for institute in value_:
                for specific_document_type in specific_schedule_types:
                    links = self.__parse_links_by_type(
                        specific_document_type,
                        institute_schedule_cards[degree][institute],
                    )
                    schedule_documents.extend(
                        ScheduleDocument(
                            institute,
                            specific_document_type,
                            degree,
                            academic_calendar.get_period(
                                datetime.datetime.now().date()
                            ),
                            link,
                        )
                        for link in links
                    )

        return schedule_documents
