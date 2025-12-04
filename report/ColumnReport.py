from abc import ABC
from pydantic import BaseModel


class ColumnReport(ABC, BaseModel):
    pass

    def __str__(self):
        return "\n".join(f"{attr}: {value}" for attr, value in self.to_dict().items())
