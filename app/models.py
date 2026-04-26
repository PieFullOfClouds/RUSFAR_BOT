from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class RusfarValue:
    """
    Данные одного индекса RUSFAR
    """
    code: str                    # например RUSFAR3M
    value: Optional[str]         # значение ставки
    calc_date: Optional[str]     # дата расчёта
    source_timestamp: Optional[str]  # время из источника (если есть)
    payload_hash: str            # хэш ответа (для отслеживания изменений)

    def to_dict(self) -> dict:
        # удобно сохранять в JSON
        return asdict(self)


@dataclass
class CheckResult:
    """
    Результат сравнения старых и новых данных
    """
    code: str
    has_update: bool             # есть ли изменение
    old_value: Optional[str]
    new_value: Optional[str]
    old_date: Optional[str]
    new_date: Optional[str]
    old_hash: Optional[str]
    new_hash: Optional[str]