"""Define abstract base class for analyzers."""

from abc import ABC, abstractmethod
from typing import Optional

from analyzer.utils.FileType import FileType
from report.FullReport import FullReport


class Analyzer(ABC):
    """Calulates metrics and reports about files using data backend."""

    @abstractmethod
    def analyze_file(self, file_path: str, file_type: Optional[FileType] = None) -> FullReport:
        """Analyze a file and generate a FullReport."""
        pass

    @abstractmethod
    def generate_column_report(self, df):
        """Calculate metrics about a column."""
        pass
