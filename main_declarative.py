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


# def disable_loggers():
#     # logger_names = [logging.getLogger(name).name for name in logging.root.manager.loggerDict]
#     loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
#     # print(loggers)
#     # print(logger_names)
#     for logger in loggers:
#         if logger.name != __name__:
#             logger.disabled = True
#
#
# def list_handlers(logger: logging.Logger):
#     if logger.hasHandlers():
#         for h in logger.handlers:
#             print("handler: ", h)
#
#

LOGGER_FORMAT='%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)10s() | %(message)s'

def disable_loggers_handlers():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict if name != __name__]
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


logging.basicConfig(
    level=logging.NOTSET,
    # stream=sys.stdout,
    format=LOGGER_FORMAT
)
LOG = logging.getLogger(__name__)

DB_FILENAME = "sales.db"
#
# start from scratch
#
try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass
#
# create engine and logger
#
engine = create_engine(
    f"sqlite:///{DB_FILENAME}",
    echo=True
)
#
# disable all handlers except root
#
disable_loggers_handlers()
#
# obtain base class
#
Base = declarative_base()


#
#   define class
#
class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)


LOG.info("create_all")
Base.metadata.create_all(engine)
#
# create session
#
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
customer = Customers(
    name="Fab",
    address="meow street 9",
    email="fab@meow.com"
)

session.add(customer)
session.commit()
