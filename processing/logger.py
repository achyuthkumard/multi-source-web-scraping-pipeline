import logging
from pathlib import Path


def setup_logger():
    """
    Configure application logging.

    Logs are written both to the console and
    to logs/pipeline.log.
    """

    log_dir = Path("logs")
    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger("scraping_pipeline")

    # Prevent duplicate handlers if setup_logger()
    # is called more than once.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    # -------------------------
    # File handler
    # -------------------------

    file_handler = logging.FileHandler(
        log_dir / "pipeline.log",
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # -------------------------
    # Console handler
    # -------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger