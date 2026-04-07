from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    db_username: str
    db_password: str
    db_host: str
    cloud_bucket: str

ENV_SETTINGS = EnvironmentSettings()
