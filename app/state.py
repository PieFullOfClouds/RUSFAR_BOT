import json
from pathlib import Path
from typing import Any

# файл, где храним последнее состояние
STATE_FILE = Path("data/state.json")


def load_state() -> dict[str, Any]:
    """
    Загружаем предыдущее состояние (что уже отправляли)
    """
    STATE_FILE.parent.mkdir(exist_ok=True)

    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # если файл битый — просто начинаем заново
        return {}


def save_state(state: dict[str, Any]) -> None:
    """
    Сохраняем текущее состояние
    """
    STATE_FILE.parent.mkdir(exist_ok=True)

    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)