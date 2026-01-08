from prepo.analyzer.PolarsAnalyzer import PolarsAnalyzer
from prepo.report.BooleanColumnReport import BooleanColumnReport
from prepo.report.CovarianceReport import CovarianceReport
from prepo.report.FullReport import FullReport

import pytest
import polars as pl
from unittest import mock


@pytest.mark.parametrize(
    "file_path_fixture",
    [
        "sample_csv_file_path",
        "sample_json_file_path",
        "sample_parquet_file_path",
        "sample_excel_file_path",
    ],
)
def test_polars_analyzer_file(request, file_path_fixture):
    file_path = request.getfixturevalue(file_path_fixture)
    analyzer = PolarsAnalyzer()
    polars_full_report = analyzer.analyze_file(file_path)

    assert isinstance(polars_full_report, FullReport)
    assert isinstance(polars_full_report.covariance_report, CovarianceReport)
    assert isinstance(polars_full_report.column_reports, list)
    assert len(polars_full_report.column_reports) == 13


@mock.patch("prepo.analyzer.PolarsAnalyzer.pl.read_csv")
def test_boolean_column_report_creation(mock_read_csv: mock.MagicMock):
    mock_read_csv.return_value = pl.DataFrame({"boolean_column": [True, True, True, False, None]})
    full_report_with_boolean_column = PolarsAnalyzer().analyze_file(".csv")
    assert len(full_report_with_boolean_column.column_reports) == 1
    assert full_report_with_boolean_column.column_reports[0] == BooleanColumnReport(
        name="boolean_column",
        true_proportion=0.6,
        false_proportion=0.19999999999999996,
        count=5,
        unique_count=3,
        null_count=1,
    )
