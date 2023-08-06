from os import environ
import sys
import logging
import subprocess
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

NAME = 'src'
DEBUG = True
COLORED_LOGS = True
LOG_DIRECTORY = './logs/'
LOG_ROTATION_TIME = 'midnight'
LOG_INTERVAL_RATE = 1
LOG_FILE_EXTENSION = 'log'


def add_loading_bar(loading_bar):
    if hasattr(logging, 'loading_bar'):
        raise AttributeError('Loading bar already defined in logging module')

    setattr(logging, 'loading_bar', loading_bar)


def add_logging_level(level_name, level_num, method_name=None):
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError('Level "{}" already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('Method "{}" already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('Method "{}" already defined in logging class'.format(method_name))

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


class LucidLoadingBar:
    reset = "\033[38;2;200;200;200m" if not sys.stdout.isatty() else ''

    def __init__(
            self, iterable=None, prefix='Loading...', prefix_color=None, suffix='',
            suffix_color=None, bar_color=None, percent_color=None, decimals=1,
            length=100, fill=None, print_end='\r', is_loading=None, total=0, bar_format=None
    ):
        self.iterable = iterable
        self.prefix = prefix
        self.prefix_color = prefix_color
        self.suffix = suffix
        self.suffix_color = suffix_color
        self.bar_color = "\033[38;2;0;255;255m" if not sys.stdout.isatty() else ''
        self.percent_color = percent_color
        self.decimals = decimals
        self.length = length
        self.fill = '\xdb' if environ.get('SHELL') else '\u2588'
        self.print_end = print_end
        self.is_loading = is_loading
        self.progress = 0
        self.total = total
        self.bar_format = "$RESET$PREFIX_COLOR$PREFIX$RESET |$BAR_COLOR$BAR$RESET| $PERCENT_COLOR$PERCENT$RESET"

    def get_bar(self):
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.progress / float(self.total)))
        filled_length = int(self.length * self.progress // self.total)
        bar = self.fill * filled_length + "-" * (self.length - filled_length)

        return self.format_bar(bar=bar, percent=percent)

    def get_clear_bar(self):
        return ''.join(' ' for i in range(len(self.prefix) + self.length + 9))

    def format_bar(self, bar, percent):
        formatted_bar = self.bar_format.replace(
            '$PREFIX_COLOR', self.prefix_color if self.prefix_color else ''
        ).replace(
            '$RESET', self.reset
        ).replace(
            '$PREFIX', self.prefix
        ).replace(
            '$BAR_COLOR', self.bar_color if self.bar_color else ''
        ).replace(
            '$BAR', bar
        ).replace(
            '$PERCENT_COLOR', self.percent_color if self.percent_color else ''
        ).replace(
            '$PERCENT', percent
        )

        return formatted_bar

    def init_bar(self, iterable=None, prefix="Loading...", total=None):
        try:
            tput = subprocess.Popen(['tput', 'cols'], stdout=subprocess.PIPE)
            terminal_length = int(tput.communicate()[0].strip())
        except FileNotFoundError:
            terminal_length = 100

        self.is_loading = True
        self.total = len(iterable) if iterable else total
        self.length = (terminal_length - len(self.prefix) - 10)
        self.prefix = prefix
        return self

    def finish_loading(self):
        self.is_loading = False
        self.total = 0
        self.prefix = ''
        self.progress = 0

    def progress_bar(self):
        self.progress += 1


class LucidStreamFormatter(logging.Formatter):
    reset = "\033[38;2;200;200;200m" if not sys.stdout.isatty() else ''
    white = "\033[38;2;255;255;255m" if not sys.stdout.isatty() else ''
    red = "\033[38;2;255;0;0m" if not sys.stdout.isatty() else ''
    yellow = "\033[38;2;255;255;0m" if not sys.stdout.isatty() else ''
    green = "\033[38;2;0;150;0m" if not sys.stdout.isatty() else ''
    lime = "\033[38;2;0;255;0m" if not sys.stdout.isatty() else ''
    cyan = "\033[38;2;0;255;255m" if not sys.stdout.isatty() else ''
    blue = "\033[38;2;0;0;255m" if not sys.stdout.isatty() else ''
    purple = "\033[38;2;0;0;150m" if not sys.stdout.isatty() else ''
    format = "[%(asctime)s][$COLOR%(levelname)s$RESET]$FILE$LINE %(message)s$RESET"

    FORMATS = {
        logging.CRITICAL: reset + format.replace("$COLOR", red if True else '').replace("$RESET", reset)
        .replace("$FILE", "[%(filename)s:").replace("$LINE", "%(lineno)d]"),

        logging.ERROR: reset + format.replace("$COLOR", red if True else '').replace("$RESET", reset)
        .replace("$FILE", "[%(filename)s:").replace("$LINE", "%(lineno)d]"),

        logging.WARNING: reset + format.replace("$COLOR", yellow if True else '').replace("$RESET", reset)
        .replace("$FILE", "[%(filename)s:").replace("$LINE", "%(lineno)d]"),

        logging.INFO: reset + format.replace("$COLOR", cyan if True else '').replace("$RESET", reset)
        .replace("$FILE", "").replace("$LINE", ""),

        logging.DEBUG: reset + format.replace("$COLOR", purple if True else '').replace("$RESET", reset)
        .replace("$FILE", "").replace("$LINE", ""),
    }

    def add_level_format(self, level_no, format=None):
        self.FORMATS[level_no] = format if format else self.format

    def __init__(self, format=None, datefmt=None):
        # self.format = format if format else "[%(asctime)s][$COLOR%(levelname)s$RESET]$FILE$LINE %(message)s"
        self.datefmt = datefmt if datefmt else "%m/%d/%Y %H:%M:%S"

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        formatter.datefmt = self.datefmt
        return formatter.format(record=record)


class LucidFileFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno in [logging.CRITICAL, logging.ERROR, logging.WARNING]:
            return logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s").format(record)
        return logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s").format(record)


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


add_logging_level("INIT", 15)
add_loading_bar(LucidLoadingBar())
lucid_rotating_file_handler = LucidTimedRotatingFileHandler(
    directory=LOG_DIRECTORY,
    when=LOG_ROTATION_TIME,
    interval=LOG_INTERVAL_RATE,
    file_extension=LOG_FILE_EXTENSION
)
lucid_rotating_file_handler.setFormatter(LucidFileFormatter())
lucid_stream_handler = LucidStreamHandler()
lucid_stream_handler.setFormatter(LucidStreamFormatter())
logging.basicConfig(
    level=10 if DEBUG else 15,
    handlers=[lucid_stream_handler, lucid_rotating_file_handler]
)

logger = logging.getLogger(__name__)
