import pytest


# Creating the common function for input
@pytest.fixture
def sample_csv_file_path():
    return "./tests/test_data/titanic_truncated.csv"
