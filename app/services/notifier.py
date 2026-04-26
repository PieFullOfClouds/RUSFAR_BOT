import requests


class TelegramNotifier:
    """
    Отвечает только за отправку сообщений в Telegram
    """

    def __init__(self, bot_token: str, chat_id: str, timeout: int = 20):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.timeout = timeout

    def send_message(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": text,
        }

        response = requests.post(url, data=payload, timeout=self.timeout)
        response.raise_for_status()