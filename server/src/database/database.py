from sqlalchemy import create_engine, URL, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic_settings import BaseSettings, SettingsConfigDict
class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    db_username: str
    db_password: str
    db_host: str

DATABASE_SETTINGS = DatabaseSettings()
SQLALCHEMY_URL = URL.create(
    "postgresql+psycopg2",
    username=DATABASE_SETTINGS.db_username,
    password=DATABASE_SETTINGS.db_password, # TODO put this into an .env file
    host=DATABASE_SETTINGS.db_host,
    database="modelstack"
)

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB_Base = declarative_base()

def get_database():
    db = SessionLocal()
    try:        yield db
    finally:    db.close()

class Job(DB_Base):
    __table__ = Table('jobs', DB_Base.metadata, autoload_with=engine)

class Model(DB_Base):
    __table__ = Table('models', DB_Base.metadata, autoload_with=engine)

class Dataset(DB_Base):
    __table__ = Table('datasets', DB_Base.metadata, autoload_with=engine)
