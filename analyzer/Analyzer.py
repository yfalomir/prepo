from abc import ABC, abstractmethod
from typing import Optional

from analyzer.utils.FileType import FileType
from report.FullReport import FullReport


class Analyzer(ABC):
    @abstractmethod
    def analyze_file(self, file_path: str, file_type: Optional[FileType] = None) -> FullReport:
        pass

    @abstractmethod
    def generate_column_report(self, df):
        pass
