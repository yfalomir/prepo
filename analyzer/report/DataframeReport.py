class DataframeReport:
    def __init__(
        self, path, num_rows, num_columns, column_names, dtypes, missing_values
    ):
        self.path = path
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.column_names = column_names
        self.dtypes = dtypes
        self.missing_values = missing_values
