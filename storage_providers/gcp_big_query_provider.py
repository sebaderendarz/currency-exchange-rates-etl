from typing import List

import entities
import value_objects
from storage_providers import storage_provider


class GcpBigQueryProvider(storage_provider.StorageProvider):
    def __init__(self) -> None:
        pass

    def get_latest_exchange_rates(self, source: value_objects.Source, quote_asset: str) -> List[entities.ExchangeRate]:
        pass

    def insert_exchange_rates(self, exchange_rates: List[entities.ExchangeRate]) -> None:
        pass
