from report.ColumnReport import ColumnReport


class NumericColumnReport(ColumnReport):
    name: str
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    count: int
    unique_count: int
    null_count: int

    def to_dict(self):
        return {
            "mean": self.mean,
            "median": self.median,
            "std_dev": self.std_dev,
            "min": self.min_value,
            "max": self.max_value,
            "count": self.count,
            "unique_count": self.unique_count,
            "null_count": self.null_count,
        }
