from abc import ABC

class ColumnReport(ABC):
    pass

    def __str__(self):
        return "\n".join(f"{attr}: {value}" for attr, value in self.to_dict().items())        