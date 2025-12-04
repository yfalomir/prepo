# prepo

Multibackend data exploration and preparation tool.

Using mainstream Python data manipulation libraries to compute standard metrics on your data.
Helps understand and monitore data quality over time.

## Documentation
TODO

## Get Started
```python
from analyzer.PolarsAnalyzer import PolarsAnalyzer

def main():
    
    path = "./test_data/titanic.csv"
    analyzer = PolarsAnalyzer()
    full_report= analyzer.analyze_file(path)

    print(full_report)

if __name__ == "__main__":
    main()
```

## Contributing
Contributions are welcome