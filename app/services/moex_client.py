import requests

from app.models import RusfarValue
from app.utils.hashing import stable_hash


class MoexClient:
    """
    Получает актуальные значения RUSFAR из ISS marketdata.
    """

    URL = "https://iss.moex.com/iss/engines/stock/markets/index/boards/MMIX/securities.json"

    SECURITIES = [
        "RUSFAR",
        "RUSFAR1W",
        "RUSFAR2W",
        "RUSFAR1M",
        "RUSFAR3M",
        "RUSFARCNY",
        "RUSFARCN1W",
    ]

    def __init__(self, timeout: int = 20):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "rusfar-monitor-bot/1.0",
            "Accept": "application/json",
        })

    def fetch_raw(self) -> dict:
        params = {
            "iss.only": "marketdata",
            "securities": ",".join(self.SECURITIES),
            "iss.meta": "off",
            "iss.json": "extended",
            "lang": "ru",
            "marketdata.columns": "SECID,CURRENTVALUE,TRADEDATE",
            "sort_column": "securities_order",
            "limit": 20,
            "dir": "asc",
        }

        response = self.session.get(
            self.URL,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError(f"Неожиданный формат ответа MOEX: {type(data)}")

        return data

    @staticmethod
    def _extract_marketdata(raw_data: list) -> list[dict]:
        for block in raw_data:
            if isinstance(block, dict) and "marketdata" in block:
                return block["marketdata"]

        raise ValueError("В ответе MOEX не найден блок marketdata")

    def fetch_all_indexes(self) -> list[RusfarValue]:
        raw_data = self.fetch_raw()
        marketdata = self._extract_marketdata(raw_data)

        result = []

        for item in marketdata:
            code = item.get("SECID")
            value = item.get("CURRENTVALUE")
            calc_date = item.get("TRADEDATE")

            if not code:
                continue

            payload_for_hash = {
                "code": code,
                "value": value,
                "calc_date": calc_date,
                "raw_item": item,
            }

            result.append(
                RusfarValue(
                    code=code,
                    value=str(value) if value is not None else None,
                    calc_date=str(calc_date) if calc_date is not None else None,
                    source_timestamp=None,
                    payload_hash=stable_hash(payload_for_hash),
                )
            )

        return result

    def fetch_index(self, code: str) -> RusfarValue:
        all_values = self.fetch_all_indexes()

        for item in all_values:
            if item.code == code:
                return item

        raise ValueError(f"Индекс {code} не найден в ответе MOEX")