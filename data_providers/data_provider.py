import abc
from typing import List

import entities


class DataProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_exchange_rates(self, quote_asset: str) -> List[entities.ExchangeRate]:
        pass
