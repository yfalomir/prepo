"""Calulates metrics and reports about files using Polars."""

from typing import Callable, Optional
import polars as pl

from prepo.analyzer.Analyzer import Analyzer
from prepo.analyzer.utils.FileType import FileType
from prepo.report.BooleanColumnReport import BooleanColumnReport
from prepo.report.NumericColumnReport import NumericColumnReport
from prepo.report.StringColumnReport import StringColumnReport
from prepo.report.TemporalColumnReport import TemporalColumnReport
from prepo.report.DataframeReport import DataframeReport
from prepo.report.ColumnReport import ColumnReport
from prepo.report.FullReport import FullReport
from prepo.report.CovarianceReport import CovarianceReport


class PolarsAnalyzer(Analyzer):
    """Calulates metrics and reports about files using Polars."""

    file_type_to_reader: dict[FileType, Callable] = {
        FileType.CSV: pl.read_csv,
        FileType.JSON: pl.read_json,
        FileType.PARQUET: pl.read_parquet,
        FileType.DELTA: pl.read_delta,
        FileType.EXCEL: pl.read_excel,
    }

    def generate_dataframe_report(self, path: str, df: pl.DataFrame) -> DataframeReport:
        """Calculate a report about the dataframe."""
        return DataframeReport(
            path=path,
            num_rows=df.height,
            num_columns=df.width,
            column_names=df.columns,
            dtypes={col: str(df[col].dtype) for col in df.columns},
            missing_values={col: df[col].null_count() for col in df.columns},
        )

    def generate_numeric_column_report(self, col: str, series: pl.Series) -> NumericColumnReport:
        """Calculate a report for a numeric columns."""
        return NumericColumnReport(
            name=col,
            mean=series.mean(),
            median=series.median(),
            std_dev=series.std(),
            min_value=series.min(),
            max_value=series.max(),
            count=series.len(),
            unique_count=series.n_unique(),
            null_count=series.null_count(),
        )

    def generate_string_column_report(
        self,
        col: str,
        series: pl.Series,
    ) -> StringColumnReport:
        """Calculate a report for a text column."""
        return StringColumnReport(
            name=col,
            count=series.len(),
            unique_count=series.n_unique(),
            null_count=series.null_count(),
        )

    def generate_temporal_column_report(self, col: str, series: pl.Series) -> TemporalColumnReport:
        """Calculate a report for a temporal column."""
        return TemporalColumnReport(
            name=col,
            mean=series.mean(),
            median=series.median(),
            std_dev=series.std(),
            min_value=series.min(),
            max_value=series.max(),
            count=series.len(),
            unique_count=series.n_unique(),
            null_count=series.null_count(),
        )

    def generate_boolean_column_report(self, col: str, series: pl.Series) -> BooleanColumnReport:
        """Calculate a report for a boolean column."""
        true_count = series.sum()
        null_count = series.null_count()
        return BooleanColumnReport(
            name=col,
            true_proportion=true_count / series.len(),
            false_proportion=1 - (true_count + null_count) / series.len(),
            count=series.len(),
            unique_count=series.n_unique(),
            null_count=series.null_count(),
        )

    def generate_column_report(self, df) -> list[ColumnReport]:
        """Return adequate ColumnReport instances for each column."""
        column_reports: list[ColumnReport] = []
        for col in df.columns:
            series = df[col]

            # Generate report based on data type
            report: ColumnReport
            if series.dtype.is_numeric():
                report = self.generate_numeric_column_report(col, series)
            elif series.dtype == pl.Utf8:
                report = self.generate_string_column_report(col, series)
            elif series.dtype in (pl.Date, pl.Time, pl.Duration):
                report = self.generate_temporal_column_report(col, series)
            elif series.dtype == pl.Boolean:
                report = self.generate_boolean_column_report(col, series)
            column_reports.append(report)
        return column_reports

    def generate_covariance_report(self, df) -> CovarianceReport:
        """Calculate covariance between each pair of columns."""
        covariance_report = CovarianceReport(covariance_matrix={})
        for index, col in enumerate(df.columns):
            for covar_column in df.columns[index + 1 :]:
                covar_value = pl.cov(df[col], df[covar_column], eager=True).item(0)
                covariance_report.add_covariance(col, covar_column, covar_value)
        return covariance_report

    def analyze_file(self, file_path: str, file_type: Optional[FileType] = None) -> FullReport:
        """Analyze a file and generate a FullReport the data."""
        if file_type:
            reader = self.file_type_to_reader.get(file_type, pl.read_csv)
        elif file_path.endswith(".csv"):
            reader = pl.read_csv
        elif file_path.endswith(".json"):
            reader = pl.read_json
        elif file_path.endswith(".parquet"):
            reader = pl.read_parquet
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            reader = pl.read_excel

        df = reader(file_path)

        dataframe_report = self.generate_dataframe_report(file_path, df)
        covariance_report = self.generate_covariance_report(df)
        column_report = self.generate_column_report(df)

        return FullReport(
            dataframe_report=dataframe_report,
            covariance_report=covariance_report,
            column_reports=column_report,
        )
