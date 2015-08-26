"""
    Handlers for logger.
"""
from __future__ import with_statement

import sys
import threading
import traceback

from cytisas.logger.excs import LogProcessError
from cytisas.logger.constants import DEFAULT


class Handler(object):

    """A handler is an instance of processing the logging record"""

    def __init__(self, level=DEFAULT):
        self.lock = threading.RLock()
        self.level = level

    def process(self, record):
        """Process the record."""
        try:
            self.dispatch(record)
        except LogProcessError:
            self.handle_error(record, sys.exc_info())

    def handle_error(self, record, exc_info):
        """Handle the error when process a record"""
        try:
            traceback.print_exception(*exc_info)
            sys.stderr.write(
                '{} Logged from file {}, line {}\n'.format(
                    self.level, record.filename, record.lineno))
        except IOError as exc:
            print exc

    def dispatch(self, record):
        """Dispatch the record.

        It need to be implemented, otherwise it will raise NotImplementError.
        """
        raise NotImplementedError

    def flush(self):
        """Flushing.

        It need to be implemented, otherwise it will raise NotImplementError.
        """
        raise NotImplementedError

    def close(self):
        """Close the handler.

        It need to be implemented, otherwise it will raise NotImplementError.
        """
        raise NotImplementedError


class StreamHandler(Handler):

    """Basic Handler.

    It will log into the stream like sts.stderr.
    """

    def __init__(self, stream=None):
        Handler.__init__(self)
        if not stream:
            stream = sys.stderr
        self.stream = stream
        self.lock = threading.RLock()

    def close(self):
        """Close the stream."""
        self.stream.close()

    def flush(self):
        """Flush the data."""
        if self.stream and hasattr(self.stream, 'flush'):
            self.stream.flush()

    def dispatch(self, record):
        """Dispatch a record."""
        with self.lock:
            msg = record.msg
            msg_encode = getattr(self.stream, 'encoding', 'utf-8')
            content = msg.encode(msg_encode, 'replace')
            self.stream.write(content)
            self.flush()
