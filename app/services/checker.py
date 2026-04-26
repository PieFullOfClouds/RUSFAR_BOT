from app.constants import RUSFAR_NAMES
from app.models import CheckResult, RusfarValue


def compare_values(old_data: dict | None, new_data: RusfarValue) -> CheckResult:
    """
    Сравниваем старое состояние с новым.
    """

    old_value = old_data.get("value") if old_data else None
    old_date = old_data.get("calc_date") if old_data else None
    old_hash = old_data.get("payload_hash") if old_data else None

    has_update = (
        old_data is None
        or old_value != new_data.value
        or old_date != new_data.calc_date
        or old_hash != new_data.payload_hash
    )

    return CheckResult(
        code=new_data.code,
        has_update=has_update,
        old_value=old_value,
        new_value=new_data.value,
        old_date=old_date,
        new_date=new_data.calc_date,
        old_hash=old_hash,
        new_hash=new_data.payload_hash,
    )


def build_summary_message(results: list[CheckResult]) -> str:
    """
    Формируем одно сводное сообщение по всем обновившимся индексам.
    """

    if not results:
        return ""

    lines = ["Обновление RUSFAR", ""]

    for result in results:
        name = RUSFAR_NAMES.get(result.code, result.code)
        lines.append(f"{name}: {result.new_value} (дата: {result.new_date})")

    return "\n".join(lines)