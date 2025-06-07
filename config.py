from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_username:str
    database_password:str
    host:str
    port:str
    database:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    connection_string:str

    model_config = SettingsConfigDict(env_file="./.env")


settings = Settings()

