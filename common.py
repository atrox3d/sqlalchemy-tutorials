import logging

import sqlalchemy

LOGGER_FORMAT = '%(asctime)s | %(levelname)-5s | %(name)-24s | %(funcName)10s() | %(message)s'
external_logger = None


def setlogger(logger):
    """
    sets external module logger and returns it

    :param logger:
    :return:
    """
    global external_logger
    external_logger = logger
    return external_logger


def disable_loggers():
    """
    disable all loggers except root, main and local

    :return:
    """
    # logger_names = [logging.getLogger(name).name for name in logging.root.manager.loggerDict]
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    # print(loggers)
    # print(logger_names)
    for logger in loggers:
        if logger.name != __name__ and logger.name != "__main__":
            logger.disabled = True


def list_handlers(logger: logging.Logger):
    """
    lists logger's handlers

    :param logger:
    :return:
    """
    if logger.hasHandlers():
        for h in logger.handlers:
            print("handler: ", h)


def fix_loggers():
    """
    sets handler format and propagation for all loggers except root, main and local

    :return:
    """
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict if name != __name__ and name != "__main__"]
    for logger in loggers:
        if logger.hasHandlers():
            for handler in logger.handlers:
                # print(logger.name, handler)
                handler.formatter = logging.Formatter(
                    fmt=LOGGER_FORMAT
                )
                pass
            # logger.handlers = []
            # logger.propagate = True
            logger.propagate = False


def log_rows(rows):
    """
    logs rows of current result

    :param rows:
    :return:
    """
    if not isinstance(rows, list) and not isinstance(rows, sqlalchemy.orm.query.Query):
        rows = [rows]

    for row in rows:
        external_logger.info(f"{row.id:2d}, {row.name:<6.6s}, {row.address:<15.15s}, {row.email}")


def resetdb(filename):
    """
    delete db on start

    :param filename:
    :return:
    """
    import os
    #
    #   start from scratch
    #
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
