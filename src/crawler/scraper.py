FileTask
Represents a single downloadable file.
Fields:

file_name: Local file name.

source_url: Absolute URL to download from .

destination_path: Path relative to the download root.


class WebScraper


Constructor:
pyWebScraper(
    session: requests.Session,
    base_url: str,
    allowed_file_types: Iterable[str],
    max_depth: int,
    logger: logging.Logger,
)

Methods

crawl(start_urls: Iterable[str]) -> List[FileTask]
Performs a breadth-first crawl starting from start_urls up to max_depth, returning discovered FileTask objects.

extract_file_links(html: str, base_url: str, allowed_file_types: Iterable[str]) -> List[str](static)
Pure function that parses an HTML string and returns matching file URLs. Safe to use in tests or other pipelines.

Downloader Module
