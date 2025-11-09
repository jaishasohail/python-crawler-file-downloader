import sys
pathlib import Path

# Ensure src is on path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crawler.scraper import WebScraper  # noqa: E402


def test_extract_file_links_filters_by_extension():
    html = """

 Q1 Report
 Data
 Archive
 About

 """
    base_url = "https://example.com"

    links = WebScraper.extract_file_links(
        html=html,
        base_url=base_url,
        allowed_file_types=[".pdf", ".csv"],
    )

    assert "https://example.com/downloads/reports/Q1_2025.pdf" in links
    assert "https://example.com/downloads/data/data_set.csv" in links
    # .zip should be excluded because it's not in the allowed list
    assert "https://example.com/downloads/archive.zip" not in links
    # .html is not a downloadable file in this context
    assert all(not link.endswith(".html") for link in links)
