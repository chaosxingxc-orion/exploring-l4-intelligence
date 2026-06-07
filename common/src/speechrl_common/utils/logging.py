"""Lightweight, consistent console logging for all four works."""
from __future__ import annotations

import logging

_CONFIGURED = False
_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def get_logger(name: str = "speechrl", level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger (idempotent process-wide setup)."""
    global _CONFIGURED
    if not _CONFIGURED:
        logging.basicConfig(level=level, format=_FORMAT, datefmt="%H:%M:%S")
        _CONFIGURED = True
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
