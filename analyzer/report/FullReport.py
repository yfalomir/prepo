from analyzer.report.DataframeReport import DataframeReport
from analyzer.report.ColumnReport import ColumnReport
from analyzer.report.CovarianceReport import CovarianceReport

from typing import Optional


class FullReport:
    def __init__(
        self,
        dataframe_report: Optional[DataframeReport] = None,
        covariance_report: Optional[CovarianceReport] = None,
        column_reports: Optional[list[ColumnReport]] = None,
    ):
        self.dataframe_report: Optional[DataframeReport] = dataframe_report
        self.covariance_report: Optional[CovarianceReport] = covariance_report
        self.column_reports: list[ColumnReport] = (
            [] if column_reports is None else column_reports
        )

    def add_column_report(self, column_report: ColumnReport):
        self.column_reports.append(column_report)

    def set_dataframe_report(self, dataframe_report: DataframeReport):
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
                name = (
                    getattr(col, "name", None)
                    or getattr(col, "column", None)
                    or f"Column {idx}"
                )
                parts.append(_box(str(col), title=f"Column: {name}"))

        covariance_text = (
            str(self.covariance_report)
            if self.covariance_report is not None
            else "No covariance report"
        )
        parts.append(_box(covariance_text, title="Covariance Report"))

        return "\n\n".join(parts)
