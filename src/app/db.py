import os

from databases import Database
from sqlalchemy import (create_engine, MetaData, Integer, Column, Table, String, DateTime)
from sqlalchemy.sql import func


DATABASE_URL = os.getenv("DATABASE_URL") or "localhost"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# databases query builder
database = Database(DATABASE_URL)

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)
