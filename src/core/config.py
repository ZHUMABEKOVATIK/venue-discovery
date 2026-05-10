from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    
    DB_NAME: str
    DB_HOST: str = "localhost"
    
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"
    
    @property
    def DB_URL_PSYCOPG2(self):
        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    SECRET_KEY: str
    SECRET_KEY_ACCESS: str
    SECRET_KEY_REFRESH: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str = "HS256"

    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()