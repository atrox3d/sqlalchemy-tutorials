########################################################################################################################
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_connecting_to_database.htm
########################################################################################################################
import sqlalchemy
import os
import json
import pprint

def banner(text):
    print(80 * "#")
    print("# ", text)
    print(80 * "#")


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
    banner(title)
    print("SELECT: ", select)

    results = conn.execute(select)
    print_results(results)

    print(80 * "#")


def selectall_orm():
    """
    select all using ORM

    :return:
    """
    select = students.select()
    print_query(select, "SELECT ALL ORM")


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
print("engine.driver: ", engine.driver)

########################################################################################################################
# deprecated
# print(sqlalchemy.engine.table_names())
# deprecated
# sqlalchemy.engine.reflection.Inspector.from_engine(engine).get_table_names()
########################################################################################################################

# metadata object: contains all the definitions
meta = sqlalchemy.MetaData()

########################################################################################################################
# CREATE TABLE AND UPDATE METADATA
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
banner("CREATE ALL")
meta.create_all(engine)

########################################################################################################################
# TRY REFLECTION
########################################################################################################################
# create inspector to list tables
inspector: sqlalchemy.engine.reflection.Inspector = sqlalchemy.inspect(engine)
tablenames = inspector.get_table_names()
print("type(inspector.get_table_names()): ", type(tablenames))
print("inspector.get_table_names(): ", tablenames)

tablenames = meta.tables
banner("TABLE NAMES")
print(json.dumps(tablenames, indent=4, default=repr))

########################################################################################################################
# CRUD
########################################################################################################################
banner("INSERT OBJ")
insert = students.insert().values(name="bob")
print("insert: ", insert)
params = insert.compile().params
print("params: ", params)

########################################################################################################################
# ADD RECORD
########################################################################################################################
banner("ADD RECORD")
conn = engine.connect()
insert = students.insert().values(name="bob", lastname='lom')
print("insert: ", insert)
params = insert.compile().params
print("params: ", params)
result = conn.execute(insert)
print("result.inserted_primary_key: ", result.inserted_primary_key)

########################################################################################################################
# ADD MULTIPLE RECORDS
########################################################################################################################
banner("MULTIPLE INSERT")
result = conn.execute(
    students.insert(),
    dict(name='fab', lastname='cat'),
    dict(name='one', lastname='guy'),
    dict(name='the', lastname='mandalorian'),
    dict(name='anti', lastname='matter'),
    dict(name='mark', lastname='labby'),
    dict(name='darth', lastname='vader'),
)
print("result.inserted_primary_key_rows: ", result.inserted_primary_key_rows)

########################################################################################################################
# SELECT RECORDS
########################################################################################################################
selectall_orm()

# select records where
select = students.select().where(students.c.id > 2)
print_query(select, "SELECT WHERE")

# select function
select = sqlalchemy.sql.select([students])
print_query(select, "SELECT FUNCTION")

########################################################################################################################
# TEXT SQL
########################################################################################################################
banner("TEXT SQL")
sql = sqlalchemy.sql.text("select * from students")
print("sql: ", sql)
result = conn.execute(sql)
print_results(result)

sql = sqlalchemy.sql.text("select name, students.lastname from students where name = :name")
print("sql: ", sql)
result = conn.execute(sql, name='fab')
print_results(result)

sql = sqlalchemy.sql.text("select name, students.lastname from students where name = :name")
print("sql: ", sql)
statement = sql.bindparams(
    sqlalchemy.bindparam("name", type_=sqlalchemy.String)
)
result = conn.execute(statement, name='fab')
print_results(result)

########################################################################################################################
# SELECT + TEXT
########################################################################################################################
banner("SELECT + TEXT")
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
# SELECT + TEXT + AND
########################################################################################################################
banner("SELECT + TEXT + AND")
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
# ALIASES
########################################################################################################################
banner("ALIASES")
select = sqlalchemy.sql.text("select * from students")
print("select: ", select)
results = conn.execute(select)
print(result)

alias = students.alias("a")
select = sqlalchemy.sql.select(alias).where(alias.c.id > 2)
print(select)
result = list(conn.execute(select))
print(result)

quit()
########################################################################################################################
# UPDATE
########################################################################################################################
selectall_orm()

update = students.update().where(
    students.c.lastname == 'cat'
).values(
    lastname='boss'
)
print(update)
print(update.compile().params)
conn.execute(update)

selectalltext()
selectall_orm()
