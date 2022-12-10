import enum


class StorageType(enum.Enum):
    BIG_QUERY = "BIG_QUERY"  # GCP BigQuery
    POSTGRES = "POSTGRES"  # Postgres DB instance
