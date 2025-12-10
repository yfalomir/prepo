"""Orchestrate and aggregate reports and metrics about a dataframe."""

from pydantic import BaseModel, field_validator
from typing import Optional

from prepo.alert.Alert import Alert
from prepo.report.DataframeReport import DataframeReport
from prepo.report.ColumnReport import ColumnReport
from prepo.report.CovarianceReport import CovarianceReport


class FullReport(BaseModel):
    """Represents a comprehensive report including dataframe, covariance, and column reports."""

    dataframe_report: DataframeReport
    covariance_report: CovarianceReport
    column_reports: list[ColumnReport]

    @field_validator("column_reports", mode="before")
    @classmethod
    def ensure_list(cls, column_reports: Optional[list[ColumnReport]]) -> list[ColumnReport]:
        """Validate column_reports is a list, even if None is provided."""
        return [] if column_reports is None else column_reports

    def add_column_report(self, column_report: ColumnReport):
        """Add a column report to the column_reports."""
        self.column_reports.append(column_report)

    def set_dataframe_report(self, dataframe_report: DataframeReport):
        """Set dataframe_report."""
        self.dataframe_report = dataframe_report

    def __str__(self):
        def _box(text: str, title: str | None = None) -> str:
            lines = text.splitlines() if text is not None else [""]
            if not lines:
                lines = [""]
            if title:
                lines = [title] + ["-" * len(title)] + lines
            maxw = max(len(line) for line in lines)
            border = "+" + "-" * (maxw + 2) + "+"
            framed = [border] + [f"| {line.ljust(maxw)} |" for line in lines] + [border]
            return "\n".join(framed)

        parts = []
        df_text = (
            str(self.dataframe_report)
            if self.dataframe_report is not None
            else "No dataframe report"
        )
        parts.append(_box(df_text, title="Dataframe Report"))

        cols = self.column_reports or []
        if not cols:
            parts.append(_box("No column reports", title="Columns"))
        else:
            for idx, col in enumerate(cols, start=1):
                name = getattr(col, "name", None) or getattr(col, "column", None) or f"Column {idx}"
                parts.append(_box(str(col), title=f"Column: {name}"))

        covariance_text = (
            str(self.covariance_report)
            if self.covariance_report is not None
            else "No covariance report"
        )
        parts.append(_box(covariance_text, title="Covariance Report"))

        return "\n\n".join(parts)

    def get_dataframe_comparison_alerts(
        self,
        modified_dataframe_report: DataframeReport,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, float] = {},
    ) -> list[Alert]:
        """Return Alerts about the dataframe."""
        return self.dataframe_report.get_comparison_alerts(
            modified=modified_dataframe_report,
            default_percentage_threshold=default_percentage_threshold,
            percentage_threshold_per_column=percentage_threshold_per_column,
        )

    def get_covariance_comparison_alerts(
        self,
        modified_covariance_report: CovarianceReport,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, dict[str, float]] = {},
    ) -> list[Alert]:
        """Return Alerts about the covariances."""
        return self.covariance_report.get_comparison_alerts(
            modified=modified_covariance_report,
            default_percentage_threshold=default_percentage_threshold,
            percentage_threshold_per_column=percentage_threshold_per_column,
        )

    def get_column_comparison_alerts(
        self,
        modified_column_reports: list[ColumnReport],
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, dict[str, float]] = {},
    ) -> list[Alert]:
        """Return Alerts about all the columns."""
        alerts = []
        original_columns = {col.name: col for col in self.column_reports}
        modified_columns = {col.name: col for col in modified_column_reports}

        for col_name, original_col in original_columns.items():
            modified_col = modified_columns.get(col_name)
            if modified_col:
                col_alerts = original_col.get_comparison_alerts(
                    modified=modified_col,
                    default_percentage_threshold=default_percentage_threshold,
                    percentage_threshold_per_column=percentage_threshold_per_column.get(
                        col_name, {}
                    ),
                )
                alerts.extend(col_alerts)

        return alerts

    def get_all_comparison_alerts(
        self,
        modified_full_report: FullReport,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_dataframe: dict[str, float] = {},
        percentage_threshold_per_column: dict[str, dict[str, float]] = {},
        percentage_threshold_per_covariance: dict[str, dict[str, float]] = {},
    ) -> list[Alert]:
        """Return Alerts about all the sub-reports."""
        alerts = []

        alerts.extend(
            self.get_dataframe_comparison_alerts(
                modified_dataframe_report=modified_full_report.dataframe_report,
                default_percentage_threshold=default_percentage_threshold,
                percentage_threshold_per_column=percentage_threshold_dataframe,
            )
        )

        alerts.extend(
            self.get_covariance_comparison_alerts(
                modified_covariance_report=modified_full_report.covariance_report,
                default_percentage_threshold=default_percentage_threshold,
                percentage_threshold_per_column=percentage_threshold_per_covariance,
            )
        )

        alerts.extend(
            self.get_column_comparison_alerts(
                modified_column_reports=modified_full_report.column_reports,
                default_percentage_threshold=default_percentage_threshold,
                percentage_threshold_per_column=percentage_threshold_per_column,
            )
        )

        return alerts
