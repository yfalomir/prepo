from analyzer.report.ColumnReport import ColumnReport


class StringColumnReport(ColumnReport):
    def __init__(self, name, count, unique_count, null_count):
        self.name = name
        self.count = count
        self.unique_count = unique_count
        self.null_count = null_count

    def to_dict(self):
        return {
            "count": self.count,
            "unique_count": self.unique_count,
            "null_count": self.null_count,
        }
