import os
from typing import List

import requests

import entities
import exceptions
import value_objects
from data_providers import data_provider


class FreeCurrencyDataProvider(data_provider.DataProvider):
    URL = "https://api.freecurrencyapi.com/v1/latest"

    def __init__(self) -> None:
        self._api_key = os.environ["FREE_CURRENCY_API_KEY"]

    def get_exchange_rates(self, base_currency: str) -> List[entities.ExchangeRate]:
        params = {"apikey": self._api_key, "base_currency": base_currency}
        response = requests.get(self.URL, params=params)
        response_data = response.json()
        if response.status_code != 200:
            error_message = (
                "Request to fetch data from FreeCurrencyAPI failed with status code: "
                f"{response.status_code}. Response: {response_data}."
            )
            raise exceptions.FailedToFetchExchangeRatesFromExternalSource(error_message)
        return self._parse_response_to_exchange_rate_entites(response_data["data"], base_currency)

    def _parse_response_to_exchange_rate_entites(
        self, response_data: dict, base_currency: str
    ) -> List[entities.ExchangeRate]:
        exchange_rates = []
        for currency, exchange_rate in response_data.items():
            exchange_rate = entities.ExchangeRate(
                currency=currency,
                base_currency=base_currency,
                # Tested locally. API returns exchange rates with decimal precision 6 for all currencies.
                exchange_rate=str(exchange_rate),
                source=value_objects.Source.FC_API,
            )
            exchange_rates.append(exchange_rate)
        return exchange_rates
