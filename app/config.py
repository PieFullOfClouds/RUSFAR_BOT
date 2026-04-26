import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные из .env файла в окружение
load_dotenv()


# Описываем структуру всех настроек бота
@dataclass
class Settings:
    bot_token: str              # токен Telegram-бота
    chat_id: str               # ID группы/чата
    request_timeout: int       # таймаут HTTP-запросов
    log_level: str             # уровень логирования
    check_interval_minutes: int  # интервал проверок

    # границы окна работы (по МСК)
    moscow_start_hour: int
    moscow_start_minute: int
    moscow_end_hour: int
    moscow_end_minute: int

def get_settings() -> Settings:
    """
    Читает значения из .env и возвращает объект настроек
    """
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", "").strip(),
        chat_id=os.getenv("CHAT_ID", "").strip(),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "20")),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip(),
        check_interval_minutes=int(os.getenv("CHECK_INTERVAL_MINUTES", "30")),
        moscow_start_hour=int(os.getenv("MOSCOW_START_HOUR", "12")),
        moscow_start_minute=int(os.getenv("MOSCOW_START_MINUTE", "30")),
        moscow_end_hour=int(os.getenv("MOSCOW_END_HOUR", "20")),
        moscow_end_minute=int(os.getenv("MOSCOW_END_MINUTE", "0")),
    )