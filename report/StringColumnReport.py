from __future__ import annotations
from typing import Self
from alert.Alert import Alert
from report.ColumnReport import ColumnReport


class StringColumnReport(ColumnReport):
    name: str
    count: int
    unique_count: int
    null_count: int

    def get_comparison_alerts(
        self,
        modified: Self,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, float] = {},
    ) -> list[Alert]:
        super().get_comparison_alerts(
            modified, default_percentage_threshold, percentage_threshold_per_column
        )

        metrics_map = {
            "count": "Row count value",
            "unique_count": "Unique values count",
            "null_count": "Null count",
        }

        alerts = []
        for field, label in metrics_map.items():
            alert = self._calculate_change_alert(
                curr_val=getattr(self, field),
                new_val=getattr(modified, field),
                field_name=field,
                display_name=label,
                threshold_map=percentage_threshold_per_column,
                default_threshold=default_percentage_threshold,
            )

            if alert:
                alerts.append(alert)
        return alerts
