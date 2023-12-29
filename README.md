# pyreport
Generate reports from iterators 

## Usecase

The idea is to wrap an iterator in a reporting object.  Then configure the reporting object with the columns to report on.  Technically the records can be any type of object.

Since under the hood each column value to report on is a lambda method.  You can customize how each column value is returned.

### Example

```
from pyreport import Report

items = [
    {
        "Name": "Foo",
        "Type": 1
    },
    {
        "Name": "Bar",
        "Type": 2
    }
]

report = Report(items)
report.add_column("Name")
report.add_column("Type x 5", lambda record : record["Type"] * 5)

report.save_to_csv("report.csv")
report.save_to_tsv("report.tsv")
report.save_to_jsonl("report.jsonl")
```
