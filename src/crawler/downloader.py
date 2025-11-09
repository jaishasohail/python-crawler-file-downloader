ad_file(task, session, base_download_dir, logger, timeout=30, chunk_size=8192, retries=3) -> dict
Downloads a single file:

Creates directories as needed.

Streams content to disk.

Retries transient failures.

Returns a result dict:

json{
    "file_name": "report_Q1_2025.pdf",
    "source_url": "https://example.com/downloads/reports/Q1_2025.pdf",
    "destination_path": "./data/downloads/downloads/reports/Q1_2025.pdf",
    "status": "downloaded",
    "timestamp": 1731158400000
}

status is "downloaded" on success, "failed" on error.
download_files(tasks, session, base_download_dir, logger, max_workers=4, timeout=30) -> List[dict]
Downloads multiple FileTask objects concurrently using a thread pool.

Utilities
