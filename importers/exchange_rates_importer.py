import copy
import datetime
from typing import List, Optional

import data_providers
import entities
import exceptions
import storage_providers
import value_objects


class ExchangeRatesImporter:
    def __init__(
        self,
        source: value_objects.Source,
        storage_type: value_objects.StorageType,
        base_currency: str,
    ) -> None:
        self._source = source
        self._base_currency = base_currency
        # strategy pattern
        self._init_storage_provider(storage_type)
        self._init_data_provider()

    def _init_storage_provider(self, storage_type: value_objects.StorageType) -> None:
        if storage_type == value_objects.StorageType.GCP_BIG_QUERY:
            self._storage = storage_providers.GcpBigQueryProvider()
        elif storage_type == value_objects.StorageType.POSTGRES:
            self._storage = storage_providers.PostgresProvider()
        elif storage_type == value_objects.StorageType.SQLITE:
            self._storage = storage_providers.SqliteProvider()
        else:
            raise NotImplementedError

    def _init_data_provider(self) -> None:
        if self._source == value_objects.Source.ECB:
            self._data_provider = data_providers.EcbDataProvider()
        elif self._source == value_objects.Source.FC_API:
            self._data_provider = data_providers.FreeCurrencyDataProvider()
        else:
            raise NotImplementedError

    def run_import(self) -> None:
        latest_exchange_rates_in_db = self._storage.get_latest_exchange_rates(self._source, self._base_currency)
        try:
            new_exchange_rates = self._data_provider.get_exchange_rates(self._base_currency)
        except exceptions.FailedToFetchExchangeRatesFromExternalSource as exc:
            print(
                f"{exc}\nThere are no new exchange rates for source {self._source.value}. "
                "Trying to fill missing records with the latest available values from the past..."
            )
            new_exchange_rates = self._build_exchange_rates_for_today(latest_exchange_rates_in_db)
        exchange_rates_to_save = self._get_exchange_rates_to_save(new_exchange_rates, latest_exchange_rates_in_db)
        self._storage.insert_exchange_rates(exchange_rates_to_save)

    def _build_exchange_rates_for_today(
        self, latest_exchange_rates_in_db: List[entities.ExchangeRate]
    ) -> List[entities.ExchangeRate]:
        exchange_rates = copy.deepcopy(latest_exchange_rates_in_db)
        for exchange_rate in exchange_rates:
            exchange_rate.date = None
        return exchange_rates

    def _get_exchange_rates_to_save(
        self,
        new_exchange_rates: List[entities.ExchangeRate],
        latest_exchange_rates_in_db: List[entities.ExchangeRate],
    ) -> List[entities.ExchangeRate]:
        exchange_rates_to_save = []
        for exchange_rate in new_exchange_rates:
            exchange_rate.date = datetime.date.today().strftime('%Y-%m-%d')
            latest_exchange_rate_in_db = self._get_latest_exchange_rate_by_currencies(
                latest_exchange_rates_in_db, exchange_rate.currency, exchange_rate.base_currency
            )
            if latest_exchange_rate_in_db is None:
                exchange_rates_to_save.append(exchange_rate)
            else:
                exchange_rates_to_save.extend(
                    self._build_exchange_rate_history(latest_exchange_rate_in_db, exchange_rate)
                )
        return exchange_rates_to_save

    def _get_latest_exchange_rate_by_currencies(
        self, latest_exchange_rates_in_db: List[entities.ExchangeRate], currency: str, base_currency: str
    ) -> Optional[entities.ExchangeRate]:
        for exchange_rate in latest_exchange_rates_in_db:
            if exchange_rate.currency == currency and exchange_rate.base_currency == base_currency:
                return exchange_rate

    def _build_exchange_rate_history(
        self, latest_exchange_rate_in_db: entities.ExchangeRate, current_exchange_rate: entities.ExchangeRate
    ) -> List[entities.ExchangeRate]:
        exchange_rate_history = []
        if latest_exchange_rate_in_db.date >= current_exchange_rate.date:
            self._print_warning_message(current_exchange_rate)
            return exchange_rate_history
        exchange_rate_history.extend(
            self._generate_exchange_rates_for_previous_days(latest_exchange_rate_in_db, current_exchange_rate)
        )
        exchange_rate_history.append(current_exchange_rate)
        return exchange_rate_history

    def _print_warning_message(self, current_exchange_rate: entities.ExchangeRate) -> None:
        print(
            f'Exchange rate for currency {current_exchange_rate.currency}, '
            f'base_currency {current_exchange_rate.base_currency}, '
            f'source {current_exchange_rate.source.value} '
            f'and date >= than {current_exchange_rate.date} already exists in db! '
            'Skipping this exchange rate... but it should be investigated why '
            'there is already a record in db.'
        )

    def _generate_exchange_rates_for_previous_days(
        self, latest_exchange_rate_in_db: entities.ExchangeRate, current_exchange_rate: entities.ExchangeRate
    ) -> List[entities.ExchangeRate]:
        exchange_rates = []
        latest_exchange_rate_date = datetime.datetime.strptime(
            latest_exchange_rate_in_db.date, '%Y-%m-%d'
        ) + datetime.timedelta(days=1)
        current_exchange_rate_date = datetime.datetime.strptime(current_exchange_rate.date, '%Y-%m-%d')
        while latest_exchange_rate_date < current_exchange_rate_date:
            exchange_rate = copy.deepcopy(latest_exchange_rate_in_db)
            exchange_rate.date = latest_exchange_rate_date.strftime('%Y-%m-%d')
            exchange_rates.append(exchange_rate)
            latest_exchange_rate_date = latest_exchange_rate_date + datetime.timedelta(days=1)
        return exchange_rates
