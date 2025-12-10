from prepo.analyzer.PolarsAnalyzer import PolarsAnalyzer
from prepo.report.CovarianceReport import CovarianceReport
from prepo.report.FullReport import FullReport
import pytest


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
