from report.StringColumnReport import StringColumnReport


def test_string_column_report_comparison():
    original_numeric_column_report = StringColumnReport(
        name="original",
        count=786,
        unique_count=10,
        null_count=5,
    )
    modified_numeric_column_report = StringColumnReport(
        name="modified",
        count=1786,
        unique_count=1000,
        null_count=500,
    )

    alerts = original_numeric_column_report.get_comparison_alerts(
        modified=modified_numeric_column_report, default_percentage_threshold=0.1
    )

    assert len(alerts) == 3

    assert any(
        "Column original: Row count value changed from 786 to 1786" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Unique values count changed from 10 to 1000" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Null count changed from 5 to 500" == alert.message for alert in alerts
    )

    assert all(alert.level == "warning" for alert in alerts)
