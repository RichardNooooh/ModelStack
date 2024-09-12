from sqlalchemy import Table, create_engine, URL, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    db_username: str
    db_password: str
    db_host: str
    db_port: int

DATABASE_SETTINGS = DatabaseSettings()
SQLALCHEMY_URL = URL.create(
    "postgresql+psycopg2",
    username=DATABASE_SETTINGS.db_username,
    password=DATABASE_SETTINGS.db_password, # TODO put this into an .env file
    host=DATABASE_SETTINGS.db_host,
    port=DATABASE_SETTINGS.db_port,
    database="modelstack"
)

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB_Base = declarative_base()

class DB_Job(DB_Base):
    __table__ = Table('jobs', DB_Base.metadata, autoload_with=engine)

