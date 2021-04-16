# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_connecting_to_database.htm
import sqlalchemy
import os
import json
import pprint


def print_results(results, title="RESULTS"):
    """
    prints formatted rows in results

    :param results:
    :param title:
    :return:
    """
    print("RESULTS: ", results)

    lresults = list(results)
    print("LRESULTS: ", lresults)

    for row in lresults:
        print(f"{title}| ", row)


def print_query(select, title):
    """
    print select output

    :param select:
    :param title:
    :return:
    """
    print(80 * "#")
    print(title)
    print(80 * "#")

    print("SELECT: ", select)

    results = conn.execute(select)
    print_results(results)

    print(80 * "#")


def selectallorm():
    """
    select all using ORM

    :return:
    """
    select = students.select()
    print_query(select, "SELECT ALL")


def selectalltext():
    """
    select all using text query

    :return:
    """
    select = sqlalchemy.sql.text("select * from students")
    print_query(select, "SELECT ALL TEXT")


DB_FILENAME = 'college.db'

# start from scratch
try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass

# create engine
engine = sqlalchemy.create_engine(
    f'sqlite:///{DB_FILENAME}',  # db file
    echo=True  # log sql statements
)
# print engine property
print(engine.driver)

# deprecated
# print(sqlalchemy.engine.table_names())
# deprecated
# sqlalchemy.engine.reflection.Inspector.from_engine(engine).get_table_names()

# metadata object: contains all the definitions
meta = sqlalchemy.MetaData()

########################################################################################################################
# create table and update metadata
########################################################################################################################
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

########################################################################################################################
# try reflection
########################################################################################################################
# create inspector to list tables
inspector: sqlalchemy.engine.reflection.Inspector = sqlalchemy.inspect(engine)
print(inspector.get_table_names())

tablenames = inspector.get_table_names()
print(type(tablenames))
print(tablenames)  # empty list
tablenames = meta.tables
pprint.pprint(tablenames.items(), indent=4)

########################################################################################################################
# CRUD
########################################################################################################################
insert = students.insert().values(name="bob")
print(insert)
params = insert.compile().params
print(params)

########################################################################################################################
# add record
########################################################################################################################
conn = engine.connect().execution_options()
insert = students.insert().values(name="bob", lastname='lom')
result = conn.execute(insert)
print(result.inserted_primary_key)

########################################################################################################################
# add multiple records
########################################################################################################################
result = conn.execute(
    students.insert(),
    dict(name='fab', lastname='cat'),
    dict(name='one', lastname='guy'),
    dict(name='the', lastname='mandalorian'),
    dict(name='anti', lastname='matter'),
    dict(name='mark', lastname='labby'),
    dict(name='darth', lastname='vader'),
)
print(result.inserted_primary_key_rows)

########################################################################################################################
# select records
########################################################################################################################
selectallorm()

# select records where
select = students.select().where(students.c.id > 2)
print_query(select, "SELECT WHERE")

# select function
select = sqlalchemy.sql.select([students])
print_query(select, "SELECT FUNCTION")

########################################################################################################################
# text sql
########################################################################################################################
sql = sqlalchemy.sql.text("select * from students")
print(sql)
result = conn.execute(sql)
print_results(result)

sql = sqlalchemy.sql.text("select name, students.lastname from students where name = :name")
print(sql)
result = conn.execute(sql, name='fab')
print_results(result)

sql = sqlalchemy.sql.text("select name, students.lastname from students where name = :name")
print(sql)
statement = sql.bindparams(
    sqlalchemy.bindparam("name", type_=sqlalchemy.String)
)
result = conn.execute(statement, name='fab')
print_results(result)

########################################################################################################################
# select + text
########################################################################################################################
select = sqlalchemy.sql.select(
    sqlalchemy.sql.text(
        "name, students.lastname from students"
    )
).where(
    sqlalchemy.sql.text(
        "name between :start and :stop"
    )
)
result = conn.execute(select, start="b", stop="t")
print_results(result)

########################################################################################################################
# select + text + and
########################################################################################################################
select = sqlalchemy.sql.select(
    sqlalchemy.sql.text(
        "name, students.lastname from students"
    )
).where(
    sqlalchemy.and_(
        sqlalchemy.sql.text(
            "name between :start and :stop"
        ),
        sqlalchemy.sql.text(
            "id > :id"
        ),
    )
)

result: sqlalchemy.engine.ResultProxy = conn.execute(
    select,
    start="b",
    stop="t",
    id=2
)
########################################################################################################################
# print(result.fetchone())
# print(result.fetchall())
# ResultProxy is closed now
########################################################################################################################
# TypeError: can only concatenate tuple (not "NoneType") to tuple
# frozen = result.freeze()
# results = frozen()
# exit()
########################################################################################################################

# so we use lists...
frozen = list(result)
print(frozen)

for row in frozen:
    print(row)

########################################################################################################################
# aliases
########################################################################################################################
select = sqlalchemy.sql.text("select * from students")
print("select: ", select)
results = conn.execute(select)
print(result)

alias = students.alias("a")
select = sqlalchemy.sql.select(alias).where(alias.c.id > 2)
print(select)
result = list(conn.execute(select))
print(result)

########################################################################################################################
# update
########################################################################################################################
selectallorm()

update = students.update().where(
    students.c.lastname == 'cat'
).values(
    lastname='boss'
)
print(update)
print(update.compile().params)
conn.execute(update)

selectalltext()
selectallorm()
