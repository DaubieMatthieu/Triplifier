import codecs
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
    try:
        with codecs.open("files/" + file_name, "r", encoding="utf8") as file:
            # get content as a list of lines (by splitting on line separators)
            content = file.read().split("\n")
            # return content as a string, by rejoining the lines (with line separators)
            # but with line number at beginning of each line (for better display)
            return '\n'.join(["{:02d}    {}".format(i + 1, content[i]) for i in range(len(content))])
    except FileNotFoundError:
        return "Could not load file '{}'".format(file_name)


def triplify(title_line_number, data_first_line_number, data_last_line_number, separator,
             data_prefix, predicate_prefix, input_file, output_file):
    # files are contained in the "files/" directory
    input_file = "files/" + input_file
    output_file = "files/" + output_file
    if not isfile(input_file):  # Checking input file exists (always the case except if the user manually erase it)
        return False, "Selected input file was not found"
    with codecs.open(input_file, "r", encoding="utf8") as csv_file:
        file_content = list(csv.reader(csv_file, delimiter=separator))
    if not file_content:
        return False, "Input file is empty"
    title_line = None
    if not title_line_number:
        # There is a title line but the user do not know where
        # We loop through the file until first non empty row
        i = 1  # Starting from first line of the file
        while not file_content[i - 1]:  # while observed line is empty
            i += 1  # skipping to next one
        title_line_number = i
        title_line = file_content[title_line_number - 1]
    else:
        title_line_number = int(title_line_number)  # parsing the value
        # checking validity
        if title_line_number < 0:
            return False, "Invalid title line number: cannot be negative"
        elif title_line_number > len(file_content):
            return False, "Invalid title line number: cannot be bigger than file length"
        elif title_line_number == 0:
            pass  # user specified code to indicate there is no title line
        else:  # the user specified the title line number
            # shifting because the first line in the file is 1 and first value of list is 0
            title_line = file_content[title_line_number - 1]
            if not title_line:
                return False, "No titles found at specified line: {}".format(title_line_number)

    if data_first_line_number:
        data_first_line_number = int(data_first_line_number)  # parsing the value
        if title_line_number and data_first_line_number < title_line_number:  # checking validity
            return False, "Data first line should be after title line"
    else:
        # The use did not specify data first line number,
        # we loop through the file until first non empty row
        i = title_line_number + 1  # starting after the title line or from 1st line if title line does not exist
        while not file_content[i - 1]:  # while observed line is empty
            i += 1  # skipping to next one
        data_first_line_number = i

    if data_last_line_number:
        data_last_line_number = int(data_last_line_number)  # parsing value
        if data_last_line_number < data_first_line_number:  # checking validity
            return False, "Data last line should be after data first line"
    else:
        data_last_line_number = len(file_content)  # by default the last line of the file

    data = file_content[data_first_line_number - 1:data_last_line_number]  # data range recovery

    return generate_output_file(title_line, data, output_file, data_prefix, predicate_prefix)


def generate_output_file(title_line, data, output_file, data_prefix, predicate_prefix):
    triplets = []

    # we do not have any way to name the subject (except with its line number which is not very informative)
    # so we use a blank node
    triplet_format = "[]    {attributes}"  # each subject will have a list of "attributes" (predicate + object)
    attribute_format = "p:{predicate}    {object}"
    spacing_line = "      "  # tabulation preceding each attribute (there is a newline for each attribute)

    for i in range(len(data)):
        row = data[i]
        if title_line and not (len(row) == len(title_line)):  # checking line validity
            return False, "Invalid columns number for data line n°{}".format(i + 1)
        attributes = []
        for j in range(len(row)):
            obj = row[j]
            if not check_float(obj):  # if value is a float, we consider it does not refer an existing object
                obj = "d:" + obj.replace(" ", "_")  # Make value url friendly
            if title_line:  # if there is a title line, we use the column name for the predicate
                predicate = "has{}".format(title_line[j].replace(" ", "_").capitalize())
            else:  # else we use a generic predicate
                predicate = "hasAttribute"
            attribute = attribute_format.format(predicate=predicate, object=obj)
            attributes.append(attribute)
        # we add the triplet, the attributes need to be separated by a ';' (for syntax) and a newline (for display)
        triplets.append(triplet_format.format(attributes=(";\n" + spacing_line).join(attributes)))

    with codecs.open(output_file, "w", encoding="utf8") as ttl_file:
        # Adding the two prefixes, separated by a newline and an additional newline before triplets
        ttl_file.write("@prefix d: <{}> .\n".format(data_prefix))
        ttl_file.write("@prefix p: <{}> .\n\n".format(predicate_prefix))
        # Triplets are separated by a "." (syntax) and a newline (display)
        ttl_file.writelines([str(line) + " .\n" for line in triplets])

    return True, "Successfully triplified file !"


def check_float(potential_float):
    # return True if the given object (str in our case), is parsable as a float (includes integers)
    try:
        float(potential_float)
        return True
    except ValueError:
        return False
