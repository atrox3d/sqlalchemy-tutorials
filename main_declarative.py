import sys

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
import os
import logging


def disable_loggers():
    # logger_names = [logging.getLogger(name).name for name in logging.root.manager.loggerDict]
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    # print(loggers)
    # print(logger_names)
    for logger in loggers:
        if logger.name != __name__:
            logger.disabled = True


def list_handlers(logger: logging.Logger):
    if logger.hasHandlers():
        for h in logger.handlers:
            print("handler: ", h)


def disable_loggers_handlers():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if logger.hasHandlers():
            for handler in logger.handlers:
                # print(logger.name, handler)
                pass
            logger.handlers = []
            # logger.propagate = True


logging.basicConfig(
    level=logging.NOTSET,
    stream=sys.stdout,
    format='%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)10s() | %(message)s'
)
LOG = logging.getLogger(__name__)

DB_FILENAME = "sales.db"

# start from scratch
try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass

engine = create_engine(
    f"sqlite:///{DB_FILENAME}",
    echo=True
)
disable_loggers_handlers()

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)


LOG.info("create_all")
# exit()
Base.metadata.create_all(engine)
