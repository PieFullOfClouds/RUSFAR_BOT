from app.config import get_settings
from app.constants import RUSFAR_CODES
from app.logger import setup_logger
from app.services.checker import compare_values, build_summary_message
from app.services.moex_client import MoexClient
from app.services.notifier import TelegramNotifier
from app.state import load_state, save_state
from app.utils.dt import now_moscow, is_in_window


def run_check() -> None:
    """
    Один цикл проверки всех индексов.
    """

    settings = get_settings()
    logger = setup_logger(settings.log_level)

    current_dt = now_moscow()

    if not is_in_window(
        current_dt,
        settings.moscow_start_hour,
        settings.moscow_start_minute,
        settings.moscow_end_hour,
        settings.moscow_end_minute,
    ):
        logger.info("Вне окна проверки")
        return

    logger.info("Старт проверки")

    state = load_state()

    client = MoexClient(timeout=settings.request_timeout)
    notifier = TelegramNotifier(
        bot_token=settings.bot_token,
        chat_id=settings.chat_id,
        timeout=settings.request_timeout,
    )

    updated_results = []
    updated_any = False

    for code in RUSFAR_CODES:
        try:
            new_data = client.fetch_index(code)
            old_data = state.get(code)

            result = compare_values(old_data, new_data)

            if result.has_update:
                updated_results.append(result)
                state[code] = new_data.to_dict()
                updated_any = True
                logger.info(f"Обновление: {code}")
            else:
                logger.info(f"Без изменений: {code}")

        except Exception as e:
            logger.exception(f"Ошибка {code}: {e}")

    if updated_any:
        message = build_summary_message(updated_results)
        notifier.send_message(message)
        save_state(state)
        logger.info("Отправлено сводное сообщение")

    logger.info("Проверка завершена")