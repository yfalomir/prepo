from prepo.report.TemporalColumnReport import TemporalColumnReport


def test_temporal_column_report_comparison():
    original_string_column_report = TemporalColumnReport(
        name="original",
        mean=10,
        median=100,
        std_dev=8.7,
        min_value=0,
        max_value=153.5,
        count=786,
        unique_count=10,
        null_count=5,
    )
    modified_string_column_report = TemporalColumnReport(
        name="modified",
        mean=2,
        median=200,
        std_dev=18.7,
        min_value=100,
        max_value=223.5,
        count=1786,
        unique_count=1000,
        null_count=500,
    )

    alerts = original_string_column_report.get_comparison_alerts(
        modified=modified_string_column_report, default_percentage_threshold=0.1
    )

    assert len(alerts) == 8

    assert any(
        "Column original: Mean changed from 10.0 to 2.0" == alert.message for alert in alerts
    )
    assert any(
        "Column original: Median changed from 100.0 to 200.0" == alert.message for alert in alerts
    )
    assert any(
        "Column original: Standard deviation changed from 8.7 to 18.7" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Minimum value changed from 0.0 to 100.0" == alert.message
        for alert in alerts
    )
    assert any(
        "Column original: Maximum value changed from 153.5 to 223.5" == alert.message
        for alert in alerts
    )
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
