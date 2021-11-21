import csv
from os import listdir
from os.path import isfile, join


def get_available_files():
    # return the csv and ttl files from the "files/" directory, separated in two lists
    files = [f for f in listdir("files") if isfile(join("files", f))]
    csv_files = [f for f in files if f.endswith(".csv")]
    ttl_files = [f for f in files if f.endswith(".ttl")]
    return csv_files, ttl_files


def get_file_content(file_name):
    with open("files/" + file_name, "r") as file:
        return file.read()


def triplify(title_line_number, data_first_line_number, data_last_line_number, separator,
             data_prefix, predicate_prefix, input_file, output_file):
    pass  # TODO
