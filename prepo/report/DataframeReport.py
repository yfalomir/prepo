"""Specify metrics about a dataframe and how to use them."""

from __future__ import annotations
from pydantic import BaseModel

from prepo.alert.Alert import Alert


class DataframeReport(BaseModel):
    """Represents the metrics of a dataframe."""

    path: str
    num_rows: int
    num_columns: int
    column_names: list[str]
    dtypes: dict[str, str]
    missing_values: dict[str, int]

    def get_comparison_alerts(
        self,
        modified: DataframeReport,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, float] = {},
    ) -> list[Alert]:
        """Calculate metrics difference and return Alerts instances depending on thresholds."""
        num_rows_diff = modified.num_rows - self.num_rows
        num_columns_diff = modified.num_columns - self.num_columns
        new_columns = set(modified.column_names) - set(self.column_names)
        removed_columns = set(self.column_names) - set(modified.column_names)
        dtype_changes = {}
        for col in set(self.column_names).intersection(set(modified.column_names)):
            original_dtype = self.dtypes.get(col)
            modified_dtype = modified.dtypes.get(col)
            if original_dtype != modified_dtype:
                dtype_changes[col] = (original_dtype, modified_dtype)
        alerts = []
        threshold = percentage_threshold_per_column.get(
            "num_rows_diff", default_percentage_threshold
        )
        if abs(num_rows_diff / max(1, self.num_rows)) > threshold:
            alerts.append(
                Alert(
                    f"Number of rows changed from {self.num_rows} to "
                    f"{modified.num_rows} ({num_rows_diff} difference)",
                    level="warning",
                )
            )

        threshold = percentage_threshold_per_column.get(
            "num_columns_diff", default_percentage_threshold
        )
        if num_columns_diff / max(1, self.num_columns) > threshold:
            alerts.append(
                Alert(
                    f"Number of columns changed from {self.num_columns}"
                    f" to {modified.num_columns} ({num_columns_diff} difference)",
                    level="warning",
                )
            )

        if new_columns != set():
            alerts.append(
                Alert(
                    f"New column{'s' if len(new_columns) > 1 else ''} "
                    f"added to dataframe: {', '.join(new_columns)}",
                    level="warning",
                )
            )

        if removed_columns != set():
            alerts.append(
                Alert(
                    f"Column{'s' if len(removed_columns) > 1 else ''} "
                    f"removed from dataframe: {', '.join(removed_columns)}",
                    level="warning",
                )
            )

        if dtype_changes != {}:
            dtype_alert_message = " \n ".join(
                f" Column {str(k)} changed from type {dtype_changes[k][0]} to {dtype_changes[k][1]}"
                for k in dtype_changes
            )
            alerts.append(
                Alert(
                    f"Column type{'s' if len(dtype_changes) > 1 else ''} changed:"
                    + dtype_alert_message,
                    level="warning",
                )
            )
        return alerts
