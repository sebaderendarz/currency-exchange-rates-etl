import abc
from typing import List

import entities
import value_objects


class StorageProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_latest_exchange_rates(self, source: value_objects.Source, quote_asset: str) -> List[entities.ExchangeRate]:
        pass

    @abc.abstractmethod
    def insert_exchange_rates(self, exchange_rates: List[entities.ExchangeRate]) -> None:
        pass
