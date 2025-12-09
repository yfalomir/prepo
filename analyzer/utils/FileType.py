"""Defines and manages supported file types."""

from enum import Enum


class FileType(Enum):
    """Supported file types."""

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    DELTA = "delta"
    EXCEL = "excel"
