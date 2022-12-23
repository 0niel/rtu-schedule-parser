from rtu_schedule_parser.constants import Degree, Institute, ScheduleType


def test_get_docs_0(schedule_downloader):
    result = schedule_downloader.get_documents()
    assert len(result) > 0
    institutes = {doc.institute for doc in result}
    degrees = {doc.degree for doc in result}
    assert Institute.IIT in institutes
    assert Institute.IKB in institutes
    assert Degree.PHD in degrees

    if (
        len(institutes) == len(Institute) and len(degrees) == len(Degree) - 1
    ):  # -1 because of college
        assert len(result) >= 4 * len(Institute) + 2 * len(Institute) + 4 * len(
            Institute
        )


def test_get_docs_1(schedule_downloader):
    result = schedule_downloader.get_documents(specific_institutes={Institute.IIT})
    institutes = {doc.institute for doc in result}
    assert len(institutes) == 1
    assert Institute.IIT in institutes


def test_get_docs_2(schedule_downloader):
    result = schedule_downloader.get_documents(
        specific_institutes={Institute.IIT, Institute.IKB},
        specific_degrees={Degree.BACHELOR, Degree.MASTER},
    )
    institutes = {doc.institute for doc in result}
    degrees = {doc.degree for doc in result}
    assert len(institutes) == 2
    assert len(degrees) == 2
    assert Institute.IIT in institutes
    assert Institute.IKB in institutes
    assert Degree.BACHELOR in degrees
    assert Degree.MASTER in degrees


def test_get_docs_3(schedule_downloader):
    result = schedule_downloader.get_documents(
        specific_degrees={Degree.BACHELOR},
        specific_schedule_types={
            ScheduleType.SEMESTER,
            ScheduleType.EXAM_SESSION,
            ScheduleType.TEST_SESSION,
        },
    )
    assert len(result) > 0
    urls = [doc.url for doc in result]
    assert "" not in urls
    assert None not in urls

    for url in urls:
        assert url.startswith("http")


def test_get_docs_4(schedule_downloader):
    result = schedule_downloader.get_documents(
        specific_degrees={Degree.BACHELOR},
        specific_schedule_types={
            ScheduleType.SEMESTER,
        },
        specific_institutes={Institute.IPTIP},
    )
    assert len(result) == 9


def test_get_docs_5(schedule_downloader):
    result = schedule_downloader.get_documents(
        specific_degrees={Degree.COLLEGE},
        specific_schedule_types={
            ScheduleType.SEMESTER,
        },
        specific_institutes={Institute.COLLEGE},
    )
    assert len(result) == 1
