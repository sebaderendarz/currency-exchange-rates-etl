from typing import List

import entities
from data_providers import data_provider


class EcbDataProvider(data_provider.DataProvider):
    def get_exchange_rates(self, quote_asset: str) -> List[entities.ExchangeRate]:
        pass
