"""
    A logging system prototype.
"""
import sys

from cytisas.logger.constants import (
    DEFAULT, DEBUG, INFO, WARNING, ERROR, CRITICAL)
from cytisas.logger.models import LogRecord


class Logger(object):

    """A Looger Class."""

    def __init__(self, name, level=DEFAULT):
        self.name = name
        self.level = level
        self.handlers = []

    def add_handler(self, handler):
        """Add a handler to a logger."""
        if handler not in self.handlers:
            self.handlers.append(handler)

    def remove_hanlder(self, handler):
        """Remove a handler from a logger."""
        if handler in self.handlers:
            self.handlers.remove(handler)

    def handle(self, record):
        """Handle the record."""
        for handler in self.handlers:
            if record.level >= handler.level:
                handler.process(record)

    def check_level(self, level):
        """Check the current level."""
        if self.level <= level:
            return True
        return False

    def _log(self, msg, level, exc_info=None):
        """Log a message."""
        kwargs = {
            "exc_info": exc_info,
            "frame": sys._getframe(1)
        }
        record = LogRecord(self.name, level, msg, kwargs)
        self.handle(record)

    def log(self, msg, level=DEFAULT):
        """Basic Log."""
        if self.check_level(level):
            self._log(msg, level)

    def debug(self, msg):
        """Debug Log."""
        if self.check_level(DEBUG):
            self._log(msg, DEBUG)

    def info(self, msg):
        """Info Log."""
        if self.check_level(INFO):
            self._log(msg, INFO)

    def warn(self, msg):
        """Warn Log."""
        if self.check_level(WARNING):
            self._log(msg, WARNING)

    def error(self, msg):
        """Error Log."""
        if self.check_level(ERROR):
            self._log(msg, ERROR)

    def critical(self, msg):
        """Critical Log."""
        if self.check_level(CRITICAL):
            self._log(msg, CRITICAL)
