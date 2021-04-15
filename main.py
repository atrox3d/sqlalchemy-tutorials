# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_connecting_to_database.htm
import sqlalchemy
from sqlalchemy import create_engine
import os

DB_FILENAME = 'college.db'

try:
    os.remove(DB_FILENAME)
except FileNotFoundError:
    pass

engine = create_engine(f'sqlite:///{DB_FILENAME}', echo=True)
print(engine.driver)
# deprecated
# print(engine.table_names())
# deprecated
# Inspector.from_engine(engine).get_table_names()
inspector: sqlalchemy.engine.reflection.Inspector = sqlalchemy.inspect(engine)
print(inspector.get_table_names())
