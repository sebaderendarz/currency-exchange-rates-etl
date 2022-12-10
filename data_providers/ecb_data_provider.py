from typing import List

import entities
from data_providers import data_provider


class EcbDataProvider(data_provider.DataProvider):
    URL = "https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A"

    def get_exchange_rates(self, base_currency: str) -> List[entities.ExchangeRate]:
        pass
