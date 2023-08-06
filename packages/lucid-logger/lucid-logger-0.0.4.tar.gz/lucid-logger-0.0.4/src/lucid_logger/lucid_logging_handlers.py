import sys
import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class LucidTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, directory, when, interval, file_extension):
        self.directory = directory
        self.when = when
        self.interval = interval
        self.file_extension = file_extension
        filename = f"{self.directory}{self.generateFileName()}.{self.file_extension}"
        TimedRotatingFileHandler.__init__(self, filename=filename, when=when, interval=interval)

    def doRollover(self):
        self.stream.close()
        self.baseFilename = f"{self.directory}{self.generateFileName()}.{self.file_extension}"
        self.stream = open(self.baseFilename, 'a')
        self.rolloverAt = self.rolloverAt + self.interval

    def generateFileName(self):
        date_format = "%Y-%m-%d %H%M%S"
        return datetime.now().strftime(date_format)


class LucidStreamHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.return_carriage = '\r'

    def emit(self, record):
        if logging.loading_bar.is_loading:
            self.stream.write(self.return_carriage + logging.loading_bar.get_clear_bar() + self.return_carriage)
        message = self.format(record)
        self.stream.write(self.return_carriage + message + self.terminator)
        if logging.loading_bar.is_loading:
            self.stream.write(self.return_carriage + logging.loading_bar.get_bar() + self.return_carriage)
