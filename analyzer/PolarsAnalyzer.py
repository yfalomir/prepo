from typing import Optional
import polars as pl

from analyzer.Analyzer import Analyzer
from analyzer.report.NumericColumnReport import NumericColumnReport
from analyzer.report.StringColumnReport import StringColumnReport
from analyzer.report.TemporalColumnReport import TemporalColumnReport
from analyzer.report.DataframeReport import DataframeReport
from analyzer.report.ColumnReport import ColumnReport
from analyzer.report.FullReport import FullReport
from analyzer.utils.FileType import FileType


class PolarsAnalyzer(Analyzer):

    file_type_to_reader : dict[FileType, callable] = {
        FileType.CSV: pl.read_csv,
        FileType.JSON: pl.read_json,
        FileType.PARQUET: pl.read_parquet,
        FileType.DELTA: pl.read_delta,
        FileType.EXCEL: pl.read_excel,
    }

    def generate_dataframe_report(self, path: str, df: pl.DataFrame) -> DataframeReport:
        """Generates a report for the entire DataFrame.
        Args:
            df (pl.DataFrame): The Polars DataFrame.
            Returns:"""
        return DataframeReport(
            path=path,
            num_rows=df.height,
            num_columns=df.width,
            column_names=df.columns,
            dtypes={col: str(df[col].dtype) for col in df.columns},
            missing_values={col: df[col].null_count() for col in df.columns},
        )

    def generate_numeric_column_report(
        self, col: str, series: pl.Series
    ) -> NumericColumnReport:
        """Generates a report for numeric columns.
        Args:
            series (pl.Series): The numeric column series.
            Returns:"""
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
        """Generates a report for string columns.
        Args:
            series (pl.Series): The string column series.
            Returns:"""
        return StringColumnReport(
            name=col,
            count=series.len(),
            unique_count=series.n_unique(),
            null_count=series.null_count(),
        )

    def generate_temporal_column_report(
        self, col: str, series: pl.Series
    ) -> TemporalColumnReport:
        """Generates a report for temporal columns.
        Args:
            series (pl.Series): The temporal column series.
            Returns:"""
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

    def generate_column_report(self, df) -> list[ColumnReport]:
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
            column_reports.append(report)
        return column_reports

    def analyze_file(self, file_path: str, file_type: Optional[FileType]) -> FullReport:
        # Read the CSV file using Polars

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
        column_report = self.generate_column_report(df)

        return FullReport(dataframe_report, column_report)
