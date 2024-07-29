from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL: str = (
    'postgresql+psycopg2://postgres_user:postgres_password@'
    'localhost:5433/logs_db'
)
DB_URL: str = (
    'postgresql+psycopg2://postgres_user:postgres_password@'
    'db_logs:5432/logs_db'
)

engine = create_engine(DB_URL) #, echo=True)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
