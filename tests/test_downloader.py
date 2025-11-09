import tempfile
import sys
pathlib import Path

# Ensure src is on path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import logging  # noqa: E402
from crawler.scraper import FileTask  # noqa: E402
from crawler.downloader import download_file  # noqa: E402


class FakeResponse:
    def __init__(self, content: bytes, status_code: int = 200):
    self._content = content
    self.status_code = status_code

    def raise_for_status(self):
    if self.status_code >= 400:
    raise RuntimeError(f"HTTP error {self.status_code}")

    def iter_content(self, chunk_size=8192):
    yield self._content

    def __enter__(self):
    return self

    def __exit__(self, exc_type, exc_val, exc_tb):
    return False


class FakeSession:
    def __init__(self, content: bytes, status_code: int = 200):
    self._content = content
    self._status_code = status_code

    def get(self, url, stream=True, timeout=30):
    return FakeResponse(self._content, self._status_code)


def test_download_file_creates_file_on_success(tmp_path: Path):
    task = FileTask(
        file_name="test_file.txt",
        source_url="https://example.com/files/test_file.txt",
        destination_path="files/test_file.txt",
    )

    session = FakeSession(content=b"hello world", status_code=200)
    logger = logging.getLogger("test_downloader")

    result = download_file(
        task=task,
        session=session,
        base_download_dir=tmp_path,
        logger=logger,
        timeout=5,
        retries=1,
    )

    dest_path = Path(result["destination_path"])
    assert result["status"] == "downloaded"
    assert dest_path.exists()
    assert dest_path.read_bytes() == b"hello world"
