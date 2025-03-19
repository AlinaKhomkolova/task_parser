from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
        Класс для загрузки конфигурации из .env-файла.
        Хранит параметры подключения к базе данных и предоставляет удобные методы
        для получения DSN-строк.
    """
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    URL: str
    TOKEN: str

    @property
    def database_url_asyncpg(self) -> str:
        """
        Возвращает DSN-строку для подключения через asyncpg (используется в SQLAlchemy).
        Формат:
        postgresql+asyncpg://user:password@host:port/dbname
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_postgres(self) -> str:
        """
        Возвращает DSN-строку для прямого подключения через asyncpg.
        Формат:
        postgresql://user:password@host:port/dbname
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def url_for_parser(self) -> str:
        return f"{self.URL}"

    @property
    def token_for_bot(self) -> str:
        return f"{self.TOKEN}"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = "allow"


settings = Settings()
