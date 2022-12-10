import datetime
from typing import Optional

import pydantic

import value_objects


class ExchangeRate(pydantic.BaseModel):
    currency: str  # iso code
    base_currency: str  # iso code
    # Rate as string because there is no requirement to store it as decimal.
    # It is easier to simply take data from response and save as string.
    # What is more, one of requirements says that data should be 'identical'
    # when compared to the data source.
    exchange_rate: str
    source: value_objects.Source
    date: Optional[datetime.date] = None
