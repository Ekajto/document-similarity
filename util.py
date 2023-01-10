import os
import pickle

from prettytable import PrettyTable


def save_groups(object, filename: str = "groups"):
    with open(filename, "wb") as f:
        pickle.dump(object, f)


def load_groups(filename: str = "groups"):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    with open(filename, "rb") as f:
        return pickle.load(f)


def create_table(matrix, headers):
    table = PrettyTable()
    headers.insert(0, "")
    table.field_names = headers
    table.title = "Document Similarity Matrix"
    for i, row in enumerate(matrix):
        table.add_row([headers[i + 1]] + row)

    return table
