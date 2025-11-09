Helpers for safe filesystem operations.

ensure_directory(path: Path) -> None
Ensures a directory exists.

sanitize_filename(filename: str) -> str
Strips invalid or unsafe characters from filenames.

sanitize_path(relative_path: str) -> Path
Applies sanitize_filename to each component of a relative path.

path_inside_directory(base_dir: Path, target_path: Path) -> Path
Ensures target_path resolves within base_dir, preventing path traversal.

Testing
Tests are located in tests / and can be run with:
bashpytest

test_scraper.py: Validates HTML file link extraction.

test_downloader.py: Ensures files are written correctly using a fake session.

test_auth.py: Verifies header and cookie configuration for authentication sessions.

arduino
# python-crawler-file-downloader/requirements.txt
```text
requests
beautifulsoup4
lxml
pytest

python-crawler-file-downloader/LICENSE
textMIT License

Copyright(c) 2025 Bitbash

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
