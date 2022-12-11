import importers
import value_objects

if __name__ == "__main__":
    importers.ExchangeRatesImporter(value_objects.Source.ECB, value_objects.StorageType.SQLITE, "EUR").run_import()
    importers.ExchangeRatesImporter(value_objects.Source.FC_API, value_objects.StorageType.SQLITE, "EUR").run_import()
