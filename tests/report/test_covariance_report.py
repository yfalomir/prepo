from report.CovarianceReport import CovarianceReport


def test_dataframe_report_comparison():
    original_report = CovarianceReport(covariance_matrix={})
    original_report.add_covariance("A", "B", 1.0)
    original_report.add_covariance("A", "C", 2.0)
    original_report.add_covariance("B", "C", 3.0)

    modified_report = CovarianceReport(covariance_matrix={})
    modified_report.add_covariance("A", "B", 9.0)
    modified_report.add_covariance("A", "C", 2.0)
    modified_report.add_covariance("B", "C", 3.0)

    alerts = original_report.get_comparison_alerts(
        modified=modified_report, default_percentage_threshold=0.1
    )

    assert len(alerts) == 1
    assert any(
        "Covariance for columns A and B changed from 1.0 to 9.0" in alert.message
        for alert in alerts
    )

    assert all(alert.level == "warning" for alert in alerts)
