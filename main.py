# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_connecting_to_database.htm
import sqlalchemy
import os

DB_FILENAME = 'college.db'

try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass

engine = sqlalchemy.create_engine(f'sqlite:///{DB_FILENAME}', echo=True)
print(engine.driver)

# deprecated
# print(sqlalchemy.engine.table_names())
# deprecated
# sqlalchemy.engine.reflection.Inspector.from_engine(engine).get_table_names()

inspector: sqlalchemy.engine.reflection.Inspector = sqlalchemy.inspect(engine)
print(inspector.get_table_names())
