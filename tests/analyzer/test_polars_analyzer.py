from prepo.analyzer.PolarsAnalyzer import PolarsAnalyzer
from prepo.report.CovarianceReport import CovarianceReport
from prepo.report.FullReport import FullReport


def test_polars_analyzer_csv_file(sample_csv_file_path):
    analyzer = PolarsAnalyzer()
    polars_full_report = analyzer.analyze_file(sample_csv_file_path)

    assert isinstance(polars_full_report, FullReport)
    assert isinstance(polars_full_report.covariance_report, CovarianceReport)
    assert isinstance(polars_full_report.column_reports, list)

    assert len(polars_full_report.column_reports) == 13
