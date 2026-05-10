import logging
import sys
import os
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Configure application-wide logging"""

    # Get log level from environment (default: INFO)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # File handler for all logs
    file_handler = logging.FileHandler(
        log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Error file handler
    error_handler = logging.FileHandler(
        log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("Ring Status Application Logging Initialized")
    logger.info(f"Log Level: {log_level}")
    logger.info(f"Log Directory: {log_dir.absolute()}")
    logger.info("=" * 80)

    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module"""
    return logging.getLogger(name)