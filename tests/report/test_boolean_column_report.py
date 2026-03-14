from prepo.report.BooleanColumnReport import BooleanColumnReport


def test_boolean_column_report_comparison():
    original_numeric_column_report = BooleanColumnReport(
        name="original",
        true_proportion=0.48,
        false_proportion=0.32,
        count=786,
        unique_count=10,
        null_count=5,
    )
    modified_numeric_column_report = BooleanColumnReport(
        name="original",
        true_proportion=0.18,
        false_proportion=0.82,
        count=1786,
        unique_count=100,
        null_count=50,
    )

    alerts = original_numeric_column_report.get_comparison_alerts(
        modified=modified_numeric_column_report, default_percentage_threshold=0.1
    )

    assert len(alerts) == 5

    assert any(
        "Column original: Proportion of True values changed from 0.48 to 0.18" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Proportion of False values changed from 0.32 to 0.82" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Row count value changed from 786 to 1786" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Unique values count changed from 10 to 100" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Null count changed from 5 to 50" == alert.message for alert in alerts
    )

    assert all(alert.level == "warning" for alert in alerts)
