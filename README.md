# prepo

Multibackend data exploration and preparation tool.
It produces structured analysis reports for dataframes and columns, and can compare reports to detect significant statistical shifts.

Backend currently supported:
- Polars

## Documentation

### Installation

Install from source:
- Clone the repo
- Run `pip install -e prepo`

### Core concepts
- Analyzer: backend-specific entry point (e.g. `PolarsAnalyzer`) that inspects a dataset and returns a reports (`ColumnReport`, `DataframeReport`, `CovarianceReport`)
- Report: structured summary of dataset- and column-level metrics; serializable to JSON.
- Comparison: result of comparing two reports objects; contains detected changes and alerts.

### Key API (high level)
- Analyzer
    - `Analyzer.analyze_file`
- Report
    - `FullReport.get_all_comparison_alerts`

### Metrics produced
- Dataframe metrics (row count, column counts, column types, etc.)
- Column metrics depending on the data type(null count, median, mean, etc.)
- Covariance metrics (covariance between each pair of columns)

### Comparison and drift detection
Each comparison alert getter allows definition of metric-wise thresholds and default threshold. If any metric drifts beyond said threshold, an alert is returned by the getter.

### Output & Integration
Reports are subclasses of Pydantic BaseModel to allow JSON-serialization and export for future use and storage.


## Examples
Analyze a file and retrieve metrics about the dataframe and its columns.
```python
from prepo import PolarsAnalyzer
    
path = "./test_data/titanic.csv"
analyzer = PolarsAnalyzer()
full_report= analyzer.analyze_file(path)

print(full_report)
```

Track data changes over time by comparing two analysis reports and receiving alerts on significant statistical shifts.
```python
from prepo import PolarsAnalyzer

analyzer = PolarsAnalyzer()

report1 = analyzer.analyze_file("./test_data/titanic.csv")
report2 = analyzer.analyze_file("./test_data/titanic_updated.csv")

comparison = report1.compare(report2)
print(comparison)
```

## Contributing
Contributions are welcome.
Please read `CONTRIBUTING.md` and open issues or discussion.