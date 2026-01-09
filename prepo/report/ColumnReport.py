"""Specify metrics about a column and how to use them."""

from abc import ABC, abstractmethod
from typing import Dict
from typing_extensions import Self
from pydantic import BaseModel

from prepo.alert.Alert import Alert


class ColumnReport(ABC, BaseModel):
    """Represents the metrics of a column in a dataframe."""

    name: str

    def __str__(self):
        return "\n".join(f"{attr}: {value}" for attr, value in self.to_dict().items())

    def _calculate_change_alert(
        self,
        curr_val: float | int,
        new_val: float | int,
        field_name: str,
        display_name: str,
        threshold_map: Dict[str, float],
        default_threshold: float,
    ) -> Alert | None:
        """Calculate metrics difference and return Alerts instances depending on thresholds."""
        # Avoid division by zero and handle 0 values logic
        denominator = max(1, abs(curr_val))

        diff_percentage = abs(new_val - curr_val) / denominator
        threshold = threshold_map.get(field_name, default_threshold)

        if diff_percentage > threshold:
            return Alert(
                f"Column {self.name}: {display_name} changed from {curr_val} to {new_val}",
                level="warning",
            )
        return None

    @abstractmethod
    def get_comparison_alerts(
        self: Self,
        modified: Self,
        default_percentage_threshold: float,
        percentage_threshold_per_column: dict[str, float],
    ) -> list[Alert]:
        """Compare two reports, checks type."""
        if type(self) is not type(modified):
            raise ValueError(f"Cannot compare {type(self)} with {type(modified)}")
        return []
