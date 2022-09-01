import os


def test_download_schedule_0(schedule_downloader):
    result = schedule_downloader.get_documents()
    document = result[0]
    path, replaced = schedule_downloader.download(document)
    assert path is not None
    assert replaced is False
    assert os.path.exists(path)
    path, replaced = schedule_downloader.download(document)
    assert path is not None
    assert replaced is False
    assert os.path.exists(path)
    with open(path, "rb") as f:
        file_size = len(f.read())
    assert file_size > 0


def test_download_schedule_1(schedule_downloader):
    result = schedule_downloader.get_documents()
    downloaded = schedule_downloader.download_all(result)
    assert len(downloaded) == len(result)
    assert len(downloaded) > 0
    for doc in downloaded:
        assert doc[1] is not None
        assert os.path.exists(doc[1])
        with open(doc[1], "rb") as f:
            file_size = len(f.read())
        assert file_size > 0
        assert doc[0] is not None
        assert doc[2] is False
