
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
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

LOGGER_FORMAT = '%(asctime)s | %(levelname)-5s | %(name)-24s | %(funcName)10s() | %(message)s'


def fix_loggers():
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
log = logging.getLogger(__name__)

DB_FILENAME = "sales.db"
#
#   start from scratch
#
try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass
#
#   create engine and logger
#
engine = create_engine(f"sqlite:///{DB_FILENAME}", echo=True)
#
#   disable all handlers except root, after logger creation
#
fix_loggers()
#
#   obtain base class
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


log.info("create_all")
Base.metadata.create_all(engine)
#
#   create session
#
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session: sqlalchemy.orm.session.Session = Session()
customer = Customers(
    name="Fab",
    address="meow street 9",
    email="fab@meow.com"
)

session.add(customer)
session.commit()

log.info("add records")
session.add_all([
    Customers(name="robb", address="here", email="email@gmail.com"),
    Customers(name="frank", address="castiglione", email="punisher@gmail.com"),
])
session.commit()
#
#   select
#
log.info("QUERY ALL")
query = session.query(Customers)
log.info(query)
result = query.all()
for row in result:
    log.info(f"{row.id:2d}, {row.name:<6.6s}, {row.address:<15.15s}, {row.email}")
#
#   update
#
log.info("QUERY.GET")
row = session.query(Customers).get(2)
log.info(f"{row.id:2d}, {row.name:<6.6s}, {row.address:<15.15s}, {row.email}")
log.info("UPDATE")
row.address = "flamingo road"
session.commit()
#
#   FIRST, EDIT, ROLLBACK
#
log.info("GET FIRST")
row = session.query(Customers).first()
log.info(f"{row.id:2d}, {row.name:<6.6s}, {row.address:<15.15s}, {row.email}")
log.info("EDIT NAME")
row.name = "JD"
log.info(f"{row.id:2d}, {row.name:<6.6s}, {row.address:<15.15s}, {row.email}")
log.info("ROLLBACK")
session.rollback()
log.info(f"{row.id:2d}, {row.name:<6.6s}, {row.address:<15.15s}, {row.email}")

