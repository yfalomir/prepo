from analyzer.report.ColumnReport import ColumnReport

class NumericColumnReport(ColumnReport):

    def __init__(self, name, mean, median, std_dev, min_value, max_value, count, unique_count, null_count):
        self.name = name
        self.mean = mean
        self.median = median
        self.std_dev = std_dev
        self.min_value = min_value
        self.max_value = max_value
        self.count = count
        self.unique_count = unique_count
        self.null_count = null_count

    def to_dict(self):
        return {
            "mean": self.mean,
            "median": self.median,
            "std_dev": self.std_dev,
            "min": self.min_value,
            "max": self.max_value,
            "count": self.count,
            "unique_count": self.unique_count,
            "null_count": self.null_count
        }