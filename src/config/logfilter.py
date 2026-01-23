"""Logging formatter and filters"""
import logging
from copy import copy


class NoTraceExceptionFormatter(logging.StreamHandler):
    """Logging formatter without traceback for exceptions"""
    def format(self, record):
        if hasattr(record, "exc_info"):
            new_record = copy(record)
            new_record.exc_info = None
            return super().format(new_record)
        return super().format(record)
