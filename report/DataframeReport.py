from pydantic import BaseModel

from alert.Alert import Alert


class DataframeReport(BaseModel):
    path: str
    num_rows: int
    num_columns: int
    column_names: list[str]
    dtypes: dict[str, str]
    missing_values: dict[str, int]


class DataframeReportComparison:
    def __init__(
        self, original: DataframeReport, modified: DataframeReport
    ) -> DataframeReportComparison:
        self.original = original
        self.modified = modified
        self.num_rows_diff = modified.num_rows - original.num_rows
        self.num_columns_diff = modified.num_columns - original.num_columns
        self.new_columns = set(modified.column_names) - set(original.column_names)
        self.removed_columns = set(original.column_names) - set(modified.column_names)
        self.dtype_changes = {}
        for col in set(original.column_names).intersection(set(modified.column_names)):
            original_dtype = original.dtypes.get(col)
            modified_dtype = modified.dtypes.get(col)
            if original_dtype != modified_dtype:
                self.dtype_changes[col] = (original_dtype, modified_dtype)

    def get_alerts(
        self,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, float] = {},
    ) -> list[Alert]:
        alerts = []
        if abs(
            self.num_rows_diff / max(1, self.original.num_rows)
        ) > percentage_threshold_per_column.get("num_rows_diff", default_percentage_threshold):
            alerts.append(
                Alert(
                    f"Number of rows changed from {self.original.num_rows} to {self.modified.num_rows} ({self.num_rows_diff} difference)",
                    level="warning",
                )
            )

        if self.num_columns_diff / max(
            1, self.original.num_columns
        ) > percentage_threshold_per_column.get("num_columns_diff", default_percentage_threshold):
            alerts.append(
                Alert(
                    f"Number of columns changed from {self.original.num_columns} to {self.modified.num_columns} ({self.num_columns_diff} difference)",
                    level="warning",
                )
            )

        if self.new_columns != set():
            alerts.append(
                Alert(
                    f"New column{'s' if len(self.new_columns) > 1 else ''} added to dataframe: {', '.join(self.new_columns)}",
                    level="warning",
                )
            )

        if self.removed_columns != set():
            alerts.append(
                Alert(
                    f"New column{'s' if len(self.removed_columns) > 1 else ''} added to dataframe: {', '.join(self.removed_columns)}",
                    level="warning",
                )
            )

        if self.dtype_changes != {}:
            dtype_alert_message = " \n ".join(
                f" Column {str(k)} changed from type {self.dtype_changes[k][0]} to {self.dtype_changes[k][1]}"
                for k in self.dtype_changes
            )
            alerts.append(
                Alert(
                    f"Column type{'s' if len(self.dtype_changes) > 1 else ''} changed:"
                    + dtype_alert_message,
                    level="warning",
                )
            )
        return alerts
