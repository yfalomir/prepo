import pytest


@pytest.fixture
def sample_csv_file_path():
    return "./tests/test_data/titanic_truncated.csv"


@pytest.fixture
def sample_json_file_path():
    return "./tests/test_data/titanic_truncated.json"


@pytest.fixture
def sample_parquet_file_path():
    return "./tests/test_data/titanic_truncated.parquet"


@pytest.fixture
def sample_excel_file_path():
    return "./tests/test_data/titanic_truncated.xlsx"
