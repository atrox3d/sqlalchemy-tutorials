from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
import logging
from common import (
    LOGGER_FORMAT,
    fix_loggers,
    log_rows,
    setlogger,
    resetdb
)

logging.basicConfig(
    level=logging.NOTSET,
    # stream=sys.stdout,
    format=LOGGER_FORMAT
)
#
#   set local logger and update common.external_logger
#
log = setlogger(logging.getLogger(__name__))

DB_FILENAME = "sales.db"
resetdb(DB_FILENAME)
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


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    custid = Column(Integer, sqlalchemy.ForeignKey('customers.id'))
    invno = Column(Integer)
    amount = Column(Integer)
    customer = sqlalchemy.orm.relationship(
        "Customer",
        back_populates="invoices"
    )


Customers.invoices = sqlalchemy.orm.relationship(
    "Invoice",
    order_by=Invoice.id,
    back_populates="customers"
)
log.info("create_all")
Base.metadata.create_all(engine)
exit()

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
