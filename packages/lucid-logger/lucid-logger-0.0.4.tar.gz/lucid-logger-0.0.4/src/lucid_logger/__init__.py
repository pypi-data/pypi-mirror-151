import logging
from src.lucid_logger import lucid_logging_formaters, lucid_logging_handlers

NAME = 'src'
DEBUG = True
COLORED_LOGS = True
LOG_DIRECTORY = './logs/'
LOG_ROTATION_TIME = 'midnight'
LOG_INTERVAL_RATE = 1
LOG_FILE_EXTENSION = 'log'

lucid_rotating_file_handler = lucid_logging_handlers.LucidTimedRotatingFileHandler(
    directory=LOG_DIRECTORY,
    when=LOG_ROTATION_TIME,
    interval=LOG_INTERVAL_RATE,
    file_extension=LOG_FILE_EXTENSION
)
lucid_rotating_file_handler.setFormatter(lucid_logging_formaters.LucidFileFormatter())
lucid_stream_handler = lucid_logging_handlers.LucidStreamHandler()
lucid_stream_handler.setFormatter(lucid_logging_formaters.LucidStreamFormatter())
logging.basicConfig(
    level=10 if DEBUG else 15,
    handlers=[lucid_stream_handler, lucid_rotating_file_handler]
)

logger = logging.getLogger(__name__)


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
