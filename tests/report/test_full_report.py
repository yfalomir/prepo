from prepo.report.FullReport import FullReport
from prepo.report.DataframeReport import DataframeReport
from prepo.report.NumericColumnReport import NumericColumnReport
from prepo.report.CovarianceReport import CovarianceReport


def test_full_report_comparison():
    original_covariance_report = CovarianceReport(covariance_matrix={})
    original_covariance_report.add_covariance("A", "B", 0.5)
    original_report = FullReport(
        dataframe_report=DataframeReport(
            path="original.csv",
            num_rows=100,
            num_columns=5,
            column_names=["A", "B"],
            dtypes={
                "A": "int",
                "B": "float",
            },
            missing_values={},
        ),
        covariance_report=original_covariance_report,
        column_reports=[
            NumericColumnReport(
                name="A",
                mean=10.0,
                median=10.0,
                std_dev=2.0,
                min_value=5.0,
                max_value=15.0,
                count=100,
                unique_count=10,
                null_count=1,
            ),
            NumericColumnReport(
                name="B",
                mean=20.0,
                median=10.0,
                std_dev=5.0,
                min_value=10.0,
                max_value=30.0,
                count=200,
                unique_count=20,
                null_count=2,
            ),
        ],
    )

    modified_covariance_report = CovarianceReport(covariance_matrix={})
    modified_covariance_report.add_covariance("A", "B", 1)
    modified_covariance_report.add_covariance("A", "C", 0.3)
    modified_report = FullReport(
        dataframe_report=DataframeReport(
            path="original.csv",
            num_rows=100,
            num_columns=5,
            column_names=["A", "B", "C"],
            dtypes={"A": "int", "B": "float", "C": "float"},
            missing_values={},
        ),
        covariance_report=modified_covariance_report,
        column_reports=[
            NumericColumnReport(
                name="A",
                mean=10.0,
                median=1000.0,
                std_dev=2.0,
                min_value=5.0,
                max_value=15.0,
                count=100,
                unique_count=10,
                null_count=1,
            ),
            NumericColumnReport(
                name="B",
                mean=20.0,
                median=10.0,
                std_dev=5.0,
                min_value=10.0,
                max_value=30.0,
                count=200,
                unique_count=20,
                null_count=2,
            ),
            NumericColumnReport(
                name="C",
                mean=0.0,
                median=10.0,
                std_dev=0.0,
                min_value=0.0,
                max_value=0.0,
                count=200,
                unique_count=20,
                null_count=2,
            ),
        ],
    )
    alerts = original_report.get_all_comparison_alerts(
        modified_full_report=modified_report, default_percentage_threshold=0.1
    )

    assert any("New column added to dataframe: C" in alert.message for alert in alerts)
    assert any("Column A: Median changed from 10.0 to 1000.0" in alert.message for alert in alerts)
    assert any(
        "Covariance for columns A and B changed from 0.5 to 1" in alert.message for alert in alerts
    )

    assert len(alerts) == 3
    assert all(alert.level == "warning" for alert in alerts)


def test_full_report_comparison_column_removed():
    original_covariance_report = CovarianceReport(covariance_matrix={})
    original_covariance_report.add_covariance("A", "B", 0.5)
    original_report = FullReport(
        dataframe_report=DataframeReport(
            path="original.csv",
            num_rows=100,
            num_columns=5,
            column_names=["A", "B"],
            dtypes={
                "A": "int",
                "B": "float",
            },
            missing_values={},
        ),
        covariance_report=original_covariance_report,
        column_reports=[
            NumericColumnReport(
                name="A",
                mean=10.0,
                median=10.0,
                std_dev=2.0,
                min_value=5.0,
                max_value=15.0,
                count=100,
                unique_count=10,
                null_count=1,
            ),
            NumericColumnReport(
                name="B",
                mean=20.0,
                median=10.0,
                std_dev=5.0,
                min_value=10.0,
                max_value=30.0,
                count=200,
                unique_count=20,
                null_count=2,
            ),
        ],
    )

    modified_covariance_report = CovarianceReport(covariance_matrix={})
    modified_report = FullReport(
        dataframe_report=DataframeReport(
            path="original.csv",
            num_rows=100,
            num_columns=5,
            column_names=["A"],
            dtypes={"A": "int"},
            missing_values={},
        ),
        covariance_report=modified_covariance_report,
        column_reports=[
            NumericColumnReport(
                name="A",
                mean=10.0,
                median=10.0,
                std_dev=2.0,
                min_value=5.0,
                max_value=15.0,
                count=100,
                unique_count=10,
                null_count=1,
            ),
        ],
    )
    alerts = original_report.get_all_comparison_alerts(
        modified_full_report=modified_report, default_percentage_threshold=0.1
    )

    assert any("Column removed from dataframe: B" in alert.message for alert in alerts)

    assert len(alerts) == 1
    assert all(alert.level == "warning" for alert in alerts)
