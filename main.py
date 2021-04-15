# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_connecting_to_database.htm
import sqlalchemy
import os
import json
import pprint

DB_FILENAME = 'college.db'

# start from scratch
try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass

# create engine
engine = sqlalchemy.create_engine(
    f'sqlite:///{DB_FILENAME}',     # db file
    echo=True                       # log sql statements
)
# print engine property
print(engine.driver)

# deprecated
# print(sqlalchemy.engine.table_names())
# deprecated
# sqlalchemy.engine.reflection.Inspector.from_engine(engine).get_table_names()

# create inspector to list tables
inspector: sqlalchemy.engine.reflection.Inspector = sqlalchemy.inspect(engine)
print(inspector.get_table_names())

# metadata object: contains all the definitions
meta = sqlalchemy.MetaData()

# create table and update metadata
students = sqlalchemy.Table(
    'students',                 # table name
    meta,                       # metadata object
    sqlalchemy.Column(          # define table column
        'id',                   # column name
        sqlalchemy.Integer,     # column type
        primary_key=True        # primary key
    ),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('lastname', sqlalchemy.String)
)

# create all tables
meta.create_all(engine)

# try reflection
tablenames = inspector.get_table_names()
print(type(tablenames))
print(tablenames)   # empty list
tablenames = meta.tables
pprint.pprint(tablenames.items(), indent=4)
