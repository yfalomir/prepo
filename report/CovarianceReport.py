from pydantic import BaseModel

from alert.Alert import Alert


class CovarianceReport(BaseModel):
    covariance_matrix: dict[str, dict[str, float]]

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

    def get_comparison_alerts(
        self,
        modified: CovarianceReport,
        default_percentage_threshold: float = 0.1,
        percentage_threshold_per_column: dict[str, dict[str, float]] = {},
    ) -> list[Alert]:
        alerts = []

        for left_column in self.covariance_matrix:
            for right_column in [
                column for column in self.covariance_matrix[left_column] if column > left_column
            ]:
                if not (
                    left_column in modified.covariance_matrix
                    and right_column in modified.covariance_matrix[left_column]
                ):
                    continue

                original_covariance = self.covariance_matrix[left_column][right_column]
                modified_covariance = modified.covariance_matrix[left_column][right_column]
                alert_threshold = percentage_threshold_per_column.get(left_column, {}).get(
                    right_column, default_percentage_threshold
                )
                if (
                    abs(modified_covariance - original_covariance) / original_covariance
                    > alert_threshold
                ):
                    alerts.append(
                        Alert(
                            f"Covariance for columns {left_column} and {right_column} changed from {original_covariance} to {modified_covariance}",
                            level="warning",
                        )
                    )
        return list(set(alerts))
