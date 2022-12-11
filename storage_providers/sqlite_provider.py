import sqlite3
from typing import List

import entities
from storage_providers import storage_provider
import value_objects


class SqliteProvider(storage_provider.StorageProvider):
    def __init__(self) -> None:
        self._init_connection()

    def _init_connection(self) -> None:
        self._conn = sqlite3.connect('exchange-rates.db')
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    currency TEXT NOT NULL,
                    base_currency TEXT NOT NULL,
                    exchange_rate TEXT NOT NULL,
                    source TEXT NOT NULL,
                    date TEXT NOT NULL
                );
            """
            )

    def get_latest_exchange_rates(
        self, source: value_objects.Source, base_currency: str
    ) -> List[entities.ExchangeRate]:
        latest_exchange_rates = []
        with self._conn:
            newest_date_per_currency = self._conn.execute(
                """
                SELECT currency, base_currency, MAX(date) AS date
                FROM exchange_rates
                WHERE base_currency = ? AND source = ?
                GROUP BY currency, base_currency
            """,
                (base_currency, source.value),
            )
            for row in newest_date_per_currency:
                exchange_rate = self._get_exchange_rate(row + (source.value,))
                latest_exchange_rates.append(exchange_rate)
        return latest_exchange_rates

    def _get_exchange_rate(self, latest_exchange_rate_info: tuple) -> entities.ExchangeRate:
        latest_exchange_rate = self._conn.execute(
            """
            SELECT * FROM exchange_rates
            WHERE
            currency = ? AND base_currency = ?
            AND date = ? AND source = ?
        """,
            latest_exchange_rate_info,
        ).fetchone()
        return entities.ExchangeRate(
            currency=latest_exchange_rate[1],
            base_currency=latest_exchange_rate[2],
            exchange_rate=latest_exchange_rate[3],
            source=value_objects.Source(latest_exchange_rate[4]),
            date=latest_exchange_rate[5],
        )

    def insert_exchange_rates(self, exchange_rates: List[entities.ExchangeRate]) -> None:
        sql = """
            INSERT INTO exchange_rates (currency, base_currency, exchange_rate, source, date)
            VALUES (?, ?, ?, ?, ?)
        """
        data = [
            (
                exchange_rate.currency,
                exchange_rate.base_currency,
                exchange_rate.exchange_rate,
                exchange_rate.source.value,
                exchange_rate.date,
            )
            for exchange_rate in exchange_rates
        ]
        with self._conn:
            self._conn.executemany(sql, data)
