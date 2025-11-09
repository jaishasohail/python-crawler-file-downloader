# Python Crawler File Downloader – API Guide

This document describes the internal modules and how to integrate or extend the crawler.

---

## Entry Point

### `src/main.py`

Command-line entry point.

#### Usage

```bash
python src/main.py --config src/config/settings.json

If settings.json is missing, the script falls back to settings.example.json.
Configuration Fields (JSON)

base_url (string, required): Root URL of the platform to mirror.

start_urls (array of strings): List of URLs to start crawling from. Defaults to [base_url].

max_depth (integer): Maximum crawl depth, where depth 0 is the start URLs.

allowed_file_types (array of strings): File extensions to download (e.g. .pdf, .csv).

download_dir (string): Path to the local downloads directory.

log_dir (string): Path to the logs directory.

concurrent_downloads (integer): Number of concurrent download workers.

timeout (integer): Request timeout for network operations, in seconds.

auth (object): Authentication configuration (see below).

Authentication Module