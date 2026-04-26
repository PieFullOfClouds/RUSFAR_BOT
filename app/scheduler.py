from apscheduler.schedulers.blocking import BlockingScheduler
from app.main import run_check


def start_scheduler():
    """
    Запускает планировщик, который вызывает run_check каждые 30 минут
    """

    scheduler = BlockingScheduler(timezone="Europe/Moscow")

    scheduler.add_job(
        run_check,
        trigger="cron",
        minute="0,30",
    )

    scheduler.start()