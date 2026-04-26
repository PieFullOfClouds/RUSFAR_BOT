import hashlib
import json


def stable_hash(data: dict) -> str:
    """
    Делаем стабильный хэш от данных
    Нужен, чтобы понять: изменилось ли что-то вообще
    """
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()