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
log_rows(result)
#
#   update
#
log.info("QUERY.GET")
row = session.query(Customers).get(2)
log_rows(row)
log.info("UPDATE")
row.address = "flamingo road"
session.commit()
#
#   FIRST, EDIT, ROLLBACK
#
log.info("GET FIRST")
row = session.query(Customers).first()
log_rows(row)

log.info("EDIT NAME")
row.name = "JD"
log_rows(row)

log.info("ROLLBACK")
session.rollback()
log_rows(row)
#
#   FILTER, UPDATE
#
log.info("FILTER")
records = session.query(Customers).filter(Customers.id != 2)
log.info(records)

log.info("UPDATE")
objects = session.query(Customers).filter(Customers.id != 2)
log_rows(objects)

count = objects.update(
    {Customers.name: "Mr." + Customers.name},
    synchronize_session=False
)
log.info(f"UPDATED {count} objects and 0 records")
log_rows(objects)

records = session.query(Customers).all()
log_rows(records)
#
#   FILTERS
#
log.info("EQUALITY")
records = session.query(Customers).filter(Customers.id == 2)
log_rows(records)

log.info("DISEQUALITY")
records = session.query(Customers).filter(Customers.id != 2)
log_rows(records)

log.info("LIKE")
records = session.query(Customers).filter(Customers.name.like("%Fa%"))
log_rows(records)

log.info("IN")
records = session.query(Customers).filter(Customers.id.in_([1,3]))
log_rows(records)

log.info("AND")
records = session.query(Customers).filter(Customers.id == 2, Customers.name.like("%robb%"))
log_rows(records)

records = session.query(Customers).filter(
    sqlalchemy.and_(
        Customers.id == 2,
        Customers.name.like("%robb%")
    )
)
log_rows(records)

log.info("OR")
records = session.query(Customers).filter(
    sqlalchemy.or_(
        Customers.id == 1,
        Customers.id == 2,
    )
)
log_rows(records)
