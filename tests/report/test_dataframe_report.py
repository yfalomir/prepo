from report.DataframeReport import DataframeReport


def test_dataframe_report_comparison():
    original_report = DataframeReport(
        path="original.csv",
        num_rows=100,
        num_columns=5,
        column_names=["A", "B", "C", "D", "E"],
        dtypes={"A": "int", "B": "float", "C": "str", "D": "bool", "E": "int"},
        missing_values={},
    )

    modified_report = DataframeReport(
        path="new.csv",
        num_rows=80,
        num_columns=6,
        column_names=["A", "B", "C", "D", "E", "F"],
        dtypes={"A": "int", "B": "float", "C": "str", "D": "bool", "E": "float", "F": "str"},
        missing_values={},
    )

    alerts = original_report.get_comparison_alerts(
        modified=modified_report, default_percentage_threshold=0.1
    )

    assert len(alerts) == 4
    assert any(
        "Number of rows changed from 100 to 80 (-20 difference)" in alert.message
        for alert in alerts
    )
    assert any(
        "Number of columns changed from 5 to 6 (1 difference)" in alert.message for alert in alerts
    )
    assert any("New column added to dataframe: F" in alert.message for alert in alerts)
    assert any(
        "Column type changed: Column E changed from type int to float" in alert.message
        for alert in alerts
    )

    assert all(alert.level == "warning" for alert in alerts)
