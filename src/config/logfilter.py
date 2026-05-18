"""Logging Handlers/Formatters for todoist-template"""
import logging
from copy import copy


class ConsoleNoTraceExceptionHandler(logging.StreamHandler):
    """Logging formatter without traceback for exceptions"""
    def format(self, record: logging.LogRecord) -> str:
        if hasattr(record, "exc_info") and record.exc_info:
            new_record = copy(record)
            new_record.exc_info = None
            return super().format(new_record)
        return super().format(record)

# ~@:-]
