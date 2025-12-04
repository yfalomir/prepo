from report.ColumnReport import ColumnReport


class StringColumnReport(ColumnReport):
    name: str
    count: int
    unique_count: int
    null_count: int

    def to_dict(self):
        return {
            "count": self.count,
            "unique_count": self.unique_count,
            "null_count": self.null_count,
        }
