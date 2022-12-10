from typing import List

import entities
from storage_providers import storage_provider
import value_objects


class GcpBigQueryProvider(storage_provider.StorageProvider):
    def __init__(self) -> None:
        pass

    def get_latest_exchange_rates(
        self, source: value_objects.Source, base_currency: str
    ) -> List[entities.ExchangeRate]:
        pass

    def insert_exchange_rates(self, exchange_rates: List[entities.ExchangeRate]) -> None:
        pass
