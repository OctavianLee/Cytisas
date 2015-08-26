"""
    Logger Model.
"""
import os
import time
import traceback
from datetime import datetime

from cytisas.logger.constants import LEVEL_NAMES

class LogRecord(object):

    """A log record is an instance of something being logged."""

    def __init__(self, logger_name, level, msg, kwargs=None):
        self.name = logger_name
        self.msg = msg
        self.level = level
        self.timestamp = time.time()
        self.exc_info = kwargs.get('exc_info')
        self.frame = kwargs.get('frame')

    @property
    def level_name(self):
        """Gets the level name."""
        return LEVEL_NAMES.get(self.level)

    @property
    def time(self):
        """Gets the utc time."""
        return datetime.utcfromtimestamp(self.timestamp)

    @property
    def calling_frame(self):
        """Gets the calling frame object."""
        frame = self.frame
        while frame:
            if frame.f_back:
                frame = frame.f_back
            break
        return frame

    @property
    def func_name(self):
        """Gets the function name of calling fram."""
        if self.calling_frame:
            return self.calling_frame.f_code.co_name

    @property
    def lineno(self):
        """Gets the line number of calling frame."""
        if self.calling_frame:
            return self.calling_frame.f_lineno

    @property
    def module(self):
        """Gets the module of calling frame."""
        if self.calling_frame:
            return self.calling_frame.f_globals.get('__name__')

    @property
    def filename(self):
        """Gets the file name of calling frame."""
        if self.calling_frame:
            return os.path.abspath(self.calling_frame.co_filename)

    def format_exception(self):
        """Gets the formated exception of calling frame."""
        if self.exc_info:
            lines = traceback.format_exception(*self.exc_info)
            return ''.join(lines).decode('utf-8', 'replace')
