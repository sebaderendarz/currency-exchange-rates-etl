from typing import List
import sqlite3

import entities
from storage_providers import storage_provider
import value_objects


class SqliteProvider(storage_provider.StorageProvider):
    def __init__(self) -> None:
        pass

    def _init_connection(self) -> None:
        self._conn = sqlite3.connect('exchange-rates.db')

    def get_latest_exchange_rates(
        self, source: value_objects.Source, base_currency: str
    ) -> List[entities.ExchangeRate]:
        raise NotImplementedError

    def insert_exchange_rates(self, exchange_rates: List[entities.ExchangeRate]) -> None:
        raise NotImplementedError
