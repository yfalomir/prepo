class CovarianceReport:
    def __init__(self, covariance_matrix: dict[str, dict[str, float]] = None):
        self.covariance_matrix: dict[str, dict[str, float]] = (
            covariance_matrix if covariance_matrix is not None else {}
        )

    def add_covariance(self, col1: str, col2: str, value: float):
        if col1 not in self.covariance_matrix:
            self.covariance_matrix[col1] = {}
        self.covariance_matrix[col1][col2] = value

        if col2 not in self.covariance_matrix:
            self.covariance_matrix[col2] = {}
        self.covariance_matrix[col2][col1] = value

    def __str__(self):
        lines = []
        sorted_cols = sorted(self.covariance_matrix.keys())
        for i, col1 in enumerate(sorted_cols):
            row = []
            for col2 in sorted_cols[:i]:
                row.append(f"{self.covariance_matrix[col1][col2]}")
            lines.append("  ".join(row))
        return "\n".join(lines)