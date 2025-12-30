"""Provide HTTP API to retrieve metrics and interact with prepo backend."""

from prepo import PolarsAnalyzer
from fastapi import FastAPI

app = FastAPI()


@app.get("/fullreport")
def get_full_report(path: str) -> dict:
    """Given a local path to a file of supported filetype return FullReport about said file."""
    analyzer = PolarsAnalyzer()
    return analyzer.analyze_file(path).model_dump()
