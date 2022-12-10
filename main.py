import importers
import value_objects

if __name__ == "__main__":
    importers.ExchangeRatesImporter(
        value_objects.Source.ECB, value_objects.StorageType.GCP_BIG_QUERY, "EUR"
    ).run_import()
    importers.ExchangeRatesImporter(
        value_objects.Source.FC_API, value_objects.StorageType.GCP_BIG_QUERY, "EUR"
    ).run_import()


# import requests     # 2.18.4
# import pandas as pd # 0.23.0
# import io

# request_url = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A'
# # Define the parameters
# parameters = {
#     'startPeriod': '2022-12-10'
# }
# response = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'})
# df = pd.read_csv(io.StringIO(response.text))
# ts = df.filter(['CURRENCY', 'OBS_VALUE'], axis=1)
# ts = ts.set_index('CURRENCY')
