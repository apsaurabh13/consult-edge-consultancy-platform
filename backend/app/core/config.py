from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SUPER_ADMIN_EMAIL: str
    SUPER_ADMIN_PASSWORD: str

    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str


    class Config:
        env_file = ".env"


settings = Settings()