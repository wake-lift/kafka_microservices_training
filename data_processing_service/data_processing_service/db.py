from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL: str = 'postgresql+psycopg2://postgres_user:postgres_password@localhost:5432/sensors_db'


class Base(DeclarativeBase):
    pass


engine = create_engine(DB_URL, echo=True)

session_factory = sessionmaker(engine)
