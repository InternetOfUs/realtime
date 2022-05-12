from wenet_realtime import config
import logging
import logging.handlers


def create_ch_handler():
    formatter = logging.Formatter(config.DEFAULT_LOGGER_FORMAT)
    ch = logging.StreamHandler()
    ch.formatter = formatter
    return ch


def create_log_file_handler():
    formatter = logging.Formatter(config.DEFAULT_LOGGER_FORMAT)
    log_file = logging.handlers.WatchedFileHandler(config.DEFAULT_LOG_FILE)
    log_file.formatter = formatter
    return log_file


def create_logger(name="wenet-undefined"):
    """create a logger with the correct configuration"""

    logger = logging.getLogger(name)
    logger.setLevel(config.DEFAULT_LOGGER_LEVEL)
    ch = create_ch_handler()
    log_file = create_log_file_handler()

    logger.addHandler(log_file)
    logger.addHandler(ch)
    return logger
