from utils.logger import get_logger
from crawler.downloader import download_files
from crawler.scraper import WebScraper, FileTask
from crawler.authenticator import create_session
from typing import Any, Dict, List
from pathlib import Path
import sys
import logging
import json
rt argparse


def load_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
    raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
    return json.load(f)


def resolve_paths(config: Dict[str, Any], project_root: Path) -> Dict[str, Any]:
    cfg = dict(config)

    download_dir = cfg.get("download_dir", "data/downloads")
    log_dir = cfg.get("log_dir", "data/logs")

    download_dir_path = Path(download_dir)
    if not download_dir_path.is_absolute():
    download_dir_path = (project_root / download_dir_path).resolve()

    log_dir_path = Path(log_dir)
    if not log_dir_path.is_absolute():
    log_dir_path = (project_root / log_dir_path).resolve()

    cfg["download_dir"] = str(download_dir_path)
    cfg["log_dir"] = str(log_dir_path)

    return cfg


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Python crawler for downloading files while mirroring directory structure."
    )
    parser.add_argument(
        "--config",
        type=str,
        default="src/config/settings.json",
        help="Path to the JSON configuration file (defaults to src/config/settings.json). "
        "If it doesn't exist, settings.example.json will be used.",
    )
    return parser.parse_args()


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    # Ensure src is on sys.path so tests and CLI work consistently
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

    args = parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
    config_path = project_root / config_path

    if not config_path.exists():
        # Fallback to example config
    example_path = project_root / "src" / "config" / "settings.example.json"
    config_path = example_path

    try:
    raw_config = load_config(config_path)
    except Exception as exc:  # pragma: no cover - hard failure path
    print(f"Failed to load configuration: {exc}")
    sys.exit(1)

    config = resolve_paths(raw_config, project_root)

    logger = get_logger("python_crawler", config["log_dir"])
    logger.info("Using configuration file at %s", config_path)

    auth_config = config.get("auth", {})
    session = create_session(auth_config, logger)

    base_url = config.get("base_url")
    if not base_url:
    logger.error("Configuration is missing 'base_url'")
    sys.exit(1)

    start_urls: List[str] = config.get("start_urls") or [base_url]
    allowed_file_types: List[str] = [
        ext.lower().strip() for ext in config.get("allowed_file_types", [])
    ]
    max_depth = int(config.get("max_depth", 1))
    concurrent_downloads = int(config.get("concurrent_downloads", 4))
    timeout = int(config.get("timeout", 30))

    scraper = WebScraper(
        session=session,
        base_url=base_url,
        allowed_file_types=allowed_file_types,
        max_depth=max_depth,
        logger=logger,
    )

    try:
    logger.info("Starting crawl from %d start URL(s)", len(start_urls))
    file_tasks: List[FileTask] = scraper.crawl(start_urls)
    except Exception as exc:  # pragma: no cover - network errors are environment-specific
    logger.exception("Error during crawling: %s", exc)
    sys.exit(1)

    if not file_tasks:
    logger.warning("No downloadable files discovered.")
    print("[]")
    return

    logger.info("Discovered %d file(s) to download.", len(file_tasks))

    try:
    results = download_files(
        tasks=file_tasks,
        session=session,
        base_download_dir=Path(config["download_dir"]),
        logger=logger,
        max_workers=concurrent_downloads,
        timeout=timeout,
    )
    except Exception as exc:  # pragma: no cover - environment-specific
    logger.exception("Error during downloading: %s", exc)
    sys.exit(1)

    # Also log a concise summary
    success_count = sum(1 for r in results if r.get("status") == "downloaded")
    fail_count = sum(1 for r in results if r.get("status") != "downloaded")
    logger.info("Download complete. Success: %d, Failed: %d",
                success_count, fail_count)

    # Print detailed JSON to stdout for automation integration
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
