import datetime
import io
from typing import List

import pandas
import requests

from data_providers import data_provider
import entities
import exceptions
import value_objects


class EcbDataProvider(data_provider.DataProvider):
    URL_TEMPLATE = "https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..{}.SP00.A"

    def get_exchange_rates(self, base_currency: str) -> List[entities.ExchangeRate]:
        params = {"startPeriod": datetime.date.today().strftime("%Y-%m-%d")}
        response = requests.get(self.URL_TEMPLATE.format(base_currency), params=params, headers={"Accept": "text/csv"})
        if response.status_code != 200:
            error_message = (
                f"Request to fetch data from {value_objects.Source.ECB.value} failed with status code: "
                f"{response.status_code}. Response: {response.text}."
            )
            raise exceptions.FailedToFetchExchangeRatesFromExternalSource(error_message)
        return self._parse_response_to_exchange_rate_entities(response.text, base_currency)

    def _parse_response_to_exchange_rate_entities(
        self, response_data: str, base_currency: str
    ) -> List[entities.ExchangeRate]:
        exchange_rates_dataframe = self._parse_response_to_dataframe(response_data)
        exchange_rates = []
        for _, record in exchange_rates_dataframe.iterrows():
            exchange_rate = entities.ExchangeRate(
                currency=record["CURRENCY"],
                base_currency=base_currency,
                # Tested locally. API returns exchange rates with decimal precision 4 for all currencies.
                exchange_rate=str(record["OBS_VALUE"]),
                source=value_objects.Source.ECB,
            )
            exchange_rates.append(exchange_rate)
        return exchange_rates

    def _parse_response_to_dataframe(self, response_data) -> pandas.DataFrame:
        try:
            exchange_rates_dataframe = pandas.read_csv(io.StringIO(response_data))
        except pandas.errors.EmptyDataError:
            error_message = f"Exchange rates missing in the response from {value_objects.Source.ECB.value}."
            raise exceptions.FailedToFetchExchangeRatesFromExternalSource(error_message)
        exchange_rates_dataframe = exchange_rates_dataframe.filter(["CURRENCY", "OBS_VALUE"], axis=1)
        if any([count > 1 for count in exchange_rates_dataframe.groupby(["CURRENCY"]).count()["OBS_VALUE"]]):
            error_message = f"Duplicated exchange rate records in the response from {value_objects.Source.ECB.value}."
            raise exceptions.FailedToFetchExchangeRatesFromExternalSource(error_message)
        return exchange_rates_dataframe
