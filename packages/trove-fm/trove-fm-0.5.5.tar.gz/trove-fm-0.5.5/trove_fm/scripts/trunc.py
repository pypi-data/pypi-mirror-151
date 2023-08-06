#!/usr/bin/env python

# from psycopg2 import DatabaseError
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from trove_fm.app.config import DATABASE_URL

engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")

target_tables = ['person', 'email_address']

# delete all table data (but keep tables)
with engine.connect() as con:
    for table in target_tables:
        statement = text(f"""DELETE FROM {table};""")
        con.execute(statement)
