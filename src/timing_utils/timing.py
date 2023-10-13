"""Timing helpers without external dependencies."""

from __future__ import annotations

from contextlib import contextmanager
import logging
import time
from functools import wraps
from typing import Callable, Iterator, Optional


LoggerLike = Optional[logging.Logger]


def _select_logger(selected: LoggerLike) -> logging.Logger:
    return selected if selected is not None else logging.getLogger(__name__)


def _elapsed_seconds(start: float, end: float) -> float:
    """Return a rounded elapsed time in seconds."""
    return round(end - start, 2)


def _emit_duration(
    log: logging.Logger, label: str, seconds: float, extra: Optional[dict]
) -> None:
    """Log a timing event with optional extra context."""
    if extra:
        log.info("%s ran in %ss", label, seconds, extra=extra)
    else:
        log.info("%s ran in %ss", label, seconds)


def timed(func_or_logger: Callable | LoggerLike = None) -> Callable:
    """
    Decorator that measures execution time.

    Supports usage as @timed or @timed().
    """

    def decorator(func: Callable, logger: LoggerLike = None) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            started = time.time()
            outcome = func(*args, **kwargs)
            finished = time.time()
            log = _select_logger(logger)
            log.debug("%s ran in %ss", func.__name__, _elapsed_seconds(started, finished))
            return outcome

        return wrapper

    if callable(func_or_logger) and not isinstance(func_or_logger, logging.Logger):
        return decorator(func_or_logger)
    return lambda func: decorator(func, logger=func_or_logger)


def time_call(func: Callable, *args, **kwargs) -> tuple[object, float]:
    """Call a function and return (result, elapsed_seconds)."""
    started = time.time()
    outcome = func(*args, **kwargs)
    finished = time.time()
    return outcome, _elapsed_seconds(started, finished)


@contextmanager
def timed_context(name: str, logger: LoggerLike = None, **kwargs) -> Iterator[None]:
    """Context manager to measure the execution time of a code block."""
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        log = _select_logger(logger)
        _emit_duration(log, name, _elapsed_seconds(start, end), kwargs or None)
