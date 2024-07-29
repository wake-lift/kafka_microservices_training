from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# DB_URL: str = (
#     'postgresql+psycopg2://postgres_user:postgres_password'
#     '@localhost:5432/sensors_db'
# )
DB_URL: str = (
    'postgresql+psycopg2://postgres_user:postgres_password@'
    'db_sensors:5432/sensors_db'
)

engine = create_engine(DB_URL)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
