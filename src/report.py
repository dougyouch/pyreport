import types
import csv
import json

class Report:
    def __init__(self, records):
        self.columns = {}
        self.records = records
        self.iterator = None
        self.row_as_dict = False

    def add_column(self, header: str, value=None):
        if value is None:
            call_method = lambda record : record[header]
        elif isinstance(value, str) or isinstance(value, int):
            call_method = lambda record : record[value]
        elif isinstance(value, types.FunctionType):
            call_method = value
        else:
            raise TypeError("unsupported value type")

        self.columns[header] = call_method

    def set_row_as_dict(self, value: bool):
        self.row_as_dict = value

    def get_headers(self) -> list:
        return list(self.columns.keys())

    def write_report(self, writer):
        self.write_header(writer)
        self.write_rows(writer)

    def write_header(self, writer):
        writer.writerow(self.get_headers())

    def write_rows(self, writer):
        writer.writerows(self)

    def save_to_csv(self, name: str):
        previous_row_as_dict, self.row_as_dict = self.row_as_dict, False

        with open(name, 'w') as csvfile:
            self.write_report(csv.writer(csvfile))

        self.row_as_dict = previous_row_as_dict

    def save_to_tsv(self, name: str):
        previous_row_as_dict, self.row_as_dict = self.row_as_dict, False

        with open(name, 'w') as csvfile:
            self.write_report(csv.writer(csvfile, delimiter="\t"))

        self.row_as_dict = previous_row_as_dict

    def save_to_jsonl(self, name: str):
        previous_row_as_dict, self.row_as_dict = self.row_as_dict, True

        with open(name, 'w') as jsonlfile:
            for row in self:
                jsonlfile.write(json.dumps(row, separators=[',', ':']) + "\n")

        self.row_as_dict = previous_row_as_dict

    def __iter__(self):
        self.iterator = iter(self.records)
        return self

    def __next__(self):
        record = next(self.iterator)

        if self.row_as_dict:
            row = {}
            for name in self.columns:
                row[name] = self.columns[name](record)
        else:
            row = []
            for name in self.columns:
                row.append(self.columns[name](record))

        return row
