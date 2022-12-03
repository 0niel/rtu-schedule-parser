import os


def test_download_schedule_0(schedule_downloader):
    result = schedule_downloader.get_documents()
    document = result[0]
    path, downloaded = schedule_downloader.download(document)
    assert path is not None
    assert downloaded is True
    assert os.path.exists(path)
    path, downloaded = schedule_downloader.download(document)
    assert path is not None
    assert downloaded is False
    assert os.path.exists(path)
    with open(path, "rb") as f:
        file_size = len(f.read())
    assert file_size > 0


def test_download_schedule_1(schedule_downloader):
    result = schedule_downloader.get_documents()
    downloaded = schedule_downloader.download_all(result)
    assert len(downloaded) == len(result)
    assert len(downloaded) > 0
    downloaded_dir = os.path.join(downloaded[0][1], "..")
    assert len(os.listdir(downloaded_dir)) == len(result)
    for doc in downloaded:
        assert doc[1] is not None
        assert os.path.exists(doc[1])
        with open(doc[1], "rb") as f:
            file_size = len(f.read())
        assert file_size > 0
        assert doc[0] is not None
        assert doc[2] is True
