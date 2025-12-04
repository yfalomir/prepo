from enum import Enum


class FileType(Enum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    DELTA = "delta"
    EXCEL = "excel"
