from datetime import datetime, time
from zoneinfo import ZoneInfo

# таймзона Москвы
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def now_moscow() -> datetime:
    """
    Текущее время в Москве
    """
    return datetime.now(MOSCOW_TZ)


def is_in_window(current_dt: datetime, start_hour, start_minute, end_hour, end_minute) -> bool:
    """
    Проверяем: сейчас в рабочем окне или нет
    """
    current_time = current_dt.timetz().replace(tzinfo=None)
    start = time(start_hour, start_minute)
    end = time(end_hour, end_minute)
    return start <= current_time <= end