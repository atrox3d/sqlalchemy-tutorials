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
    print("-" * 80)
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
    conn.execute(select)
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


def execute_decorator(f):
    def execute_wrapper(*args, **kwargs):
        print("-" * 80)

        # str_args = ", ".join(map(str, args))
        str_args = [
            arg
            if type(arg) is not dict
            else ", ".join([f"{k}={v}" for k, v in arg.items()])
            for arg in args
        ]
        lkwargs = [f"{k} = {v}" for k, v in kwargs.items()]
        str_kwargs = ", ".join(lkwargs)
        print("ARGS  | ", str_args)
        print("KWARGS| ", str_kwargs)

        print("-" * 80)

        if len(args):
            query = args[0]
            print("QUERY | ", query)
            print("PARAMS| ", query.compile().params)

        print("-" * 80)

        result = f(*args, **kwargs)
        try:
            print_results(result)
        except sqlalchemy.exc.ResourceClosedError:
            pass
        print("-" * 80)

        return result

    return execute_wrapper


DB_FILENAME = 'college.db'


def reset():
    # start from scratch
    try:
        os.remove(DB_FILENAME)
    except FileNotFoundError:
        pass


def create_engine():
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
    return engine

def create_tables(engine, meta):
    ########################################################################################################################
    # CREATE TABLE AND UPDATE METADATA
    ########################################################################################################################
    students = sqlalchemy.Table(
        'students',  # table name
        meta,  # metadata object
        sqlalchemy.Column(  # define table column
            'id',  # column name
            sqlalchemy.Integer,  # column type
            primary_key=True  # primary key
        ),
        sqlalchemy.Column('name', sqlalchemy.String),
        sqlalchemy.Column('lastname', sqlalchemy.String)
    )

    addresses = sqlalchemy.Table(
        'addresses', meta,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('st_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('students.id')),
        sqlalchemy.Column('postal_add', sqlalchemy.String),
        sqlalchemy.Column('email_add', sqlalchemy.String))

    # create all tables
    banner("CREATE ALL")
    meta.create_all(engine)
    return students, addresses


if __name__ == '__main__':

    reset()
    engine = create_engine()
    # metadata object: contains all the definitions
    meta = sqlalchemy.MetaData()
    students, addresses = create_tables(engine, meta)

    quit()
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
    conn.execute = execute_decorator(conn.execute)

    insert = students.insert().values(name="bob", lastname='lom')
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

    sql = sqlalchemy.sql.text("select name, students.lastname from students where name = :name")
    print("sql: ", sql)
    result = conn.execute(sql, name='fab')

    sql = sqlalchemy.sql.text("select name, students.lastname from students where name = :name")
    print("sql: ", sql)
    statement = sql.bindparams(
        sqlalchemy.bindparam("name", type_=sqlalchemy.String)
    )
    result = conn.execute(statement, name='fab')

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
    results = conn.execute(select)

    alias = students.alias("a")
    select = sqlalchemy.sql.select(alias).where(alias.c.id > 2)
    result = list(conn.execute(select))

    ########################################################################################################################
    # UPDATE
    ########################################################################################################################
    banner("UPDATE")
    update = students.update().where(
        students.c.lastname == 'cat'
    ).values(
        lastname='boss'
    )
    conn.execute(update)

    selectall_orm()
    ########################################################################################################################
    # DELETE
    ########################################################################################################################
    banner("DELETE")
    sdelete = students.delete().where(students.c.lastname == "lom")
    conn.execute(sdelete)
    selectall_orm()
