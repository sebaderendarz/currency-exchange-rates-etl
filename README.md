# Currency Exchange Rates ETL

App fetches currency exchange rates from FreeCurrencyAPI and European Central Bank and saves data in the data warehouse. Code also fills the gaps in the data with values from previous days when exchange rates for "today" are not available in the external source. At any point in time, in the data warehouse there should be one record per currency, base_currency, source and date. This code is meant to run once a day. When executed more times, it will print a custom error messages and skip the update of exchange rates to not create duplicates in the data warehouse.  

App can be easily extended with more data sources or storage options. You just need to add another data or storage provider class and adjust the content of `main.py` file to create an instance of importer class with correct parameters.  

In the current setup app fetches exchange rates from [FreeCurrencyAPI](https://freecurrencyapi.com/docs/latest) and [European Central Bank](https://sdw-wsrest.ecb.europa.eu/help/) and saves the data in Sqlite document db, in the `exchange-rates.db` file, in the root of the project. After the successfull execution you can review the content of the Sqlite database e.g in some online tool like [SqliteOnline](https://sqliteonline.com/). You just need to upload the `.db` file.

I strongly recommend to deep dive into the code to better understand how the currency exchange rates ETL work under the hood.

## How to run

1. Make sure you have python 3.8 installed. Consider using [Pyenv](https://github.com/pyenv/pyenv) if you want to use multiple python versions on one machine.
2. In the root directory of the project run `poetry shell`. In case you do not have poetry installed yet, check the [installation guide](https://python-poetry.org/docs/#installation).
3. Once virtual env is activated, run `poetry install` to install all needed dependencies.
4. Add env variable `export FREE_CURRENCY_API_KEY=<your api key>`. It is needed to fetch data from FreeCurrencyAPI. You can get a free API key [here](https://freecurrencyapi.com/).
5. Execute code by running `python main.py`. You can also configure a cron job to run the code e.g everyday at 6AM.

## Ideas for the future

### Add GCP BigQuery storage provider

You could store the data in GCP BigQuery instead of some relational db like Sqlite or Postgres. Firstly prepare configuration that makes it possible to communicate with GCP BigQuery by following the steps describing [how to use BigQuery client library](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries). `google-cloud-bigquery` dependency should be already installed on your machine. Check `pyproject.toml` to confirm. In the `GcpBigQueryProvider` instantiate the BigQuery Client and you can communicate with BigQuery API. Remember to create a table in BigQuery in case it is not created yet. [BigQuery Client](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries) supports SQL queries, so the integration with GCP BigQuery should be similar to the already implemented integration with `Sqlite` document db.
