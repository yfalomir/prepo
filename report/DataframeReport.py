from pydantic import BaseModel


class DataframeReport(BaseModel):
    path: str
    num_rows: int
    num_columns: int
    column_names: list[str]
    dtypes: dict[str, str]
    missing_values: dict[str, int]
