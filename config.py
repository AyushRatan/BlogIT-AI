from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    connection_string:str
    local_connection_string:str

    model_config = SettingsConfigDict(env_file="./.env")


settings = Settings()

