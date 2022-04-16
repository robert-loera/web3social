from pydantic import BaseSettings

# class to make sure we have environment variables


class Settings(BaseSettings):
  # set variable to type and default value
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
