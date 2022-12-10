import datetime
import decimal

import value_objects


class ExchangeRate:
    date: datetime.date
    base_asset: str  # iso code
    quote_asset: str  # iso code
    price: decimal.Decimal
    source: value_objects.Source
