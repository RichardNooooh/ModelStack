from sqlalchemy import Table, create_engine, URL, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from environment import ENV_SETTINGS

SQLALCHEMY_URL = URL.create(
    "postgresql+psycopg2",
    username=ENV_SETTINGS.db_username,
    password=ENV_SETTINGS.db_password, # TODO put this into an .env file
    host=ENV_SETTINGS.db_host,
    database="modelstack"
)

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB_Base = declarative_base()

class DB_Job(DB_Base):
    __table__ = Table('jobs', DB_Base.metadata, autoload_with=engine)

