"""Logging Handlers/Formatters for todoist-template"""
import logging
from copy import copy


class HttpxInfoFilter(logging.Filter):
    """Filter out INFO level messages emitted by the httpx module"""
    def filter(self, record: logging.LogRecord) -> bool:
        return not (record.name.startswith("httpx") and record.levelno == logging.INFO)


class ConsoleNoTraceExceptionHandler(logging.StreamHandler):
    """Logging formatter without traceback for exceptions"""
    def __init__(self, stream=None):
        super().__init__(stream)
        self.addFilter(HttpxInfoFilter())

    def format(self, record: logging.LogRecord) -> str:
        if hasattr(record, "exc_info") and record.exc_info:
            new_record = copy(record)
            new_record.exc_info = None
            return super().format(new_record)

        return super().format(record)

# ~@:-]
