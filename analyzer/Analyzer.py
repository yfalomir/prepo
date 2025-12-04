from abc import ABC, abstractmethod


class Analyzer(ABC):
    @abstractmethod
    def analyze_file(self):
        pass

    @abstractmethod
    def generate_column_report(self, df):
        pass
