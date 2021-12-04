import configparser
import sys
from os.path import splitext

from flask import Flask, render_template, request

import utils

app = Flask(__name__)

# loading the defaults.ini configuration file
config = configparser.ConfigParser()
config.read('defaults.ini')


# This is the main and only endpoint of the app
# It can be called with GET or POST methods, depending on the intention
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Used when calling the app without parameters (ie first load), the defaults parameters are therefore used:
        # Fetching the defaults parameters from the "defaults.ini" config file
        title_line_number = config.get("DEFAULT", "title")
        data_first_line_number = config.get("DEFAULT", "data")
        data_last_line_number = None
        separator = config.get("DEFAULT", "sep")
        data_prefix = config.get("DEFAULT", "prefix_data")
        predicate_prefix = config.get("DEFAULT", "prefix_predicate")
        input_file = None  # will select first one of the list by default
        output_file = "Automatic"  # will select "Automatic" by default
        input_file_content, output_file_content = "", ""  # not loaded before launching triplifier
        success, message = False, "Launch the Triplifier to see previews"
    else:
        # Used when calling the app with parameters (ie to triplify)
        # Fetching the parameters from the form contained in the POST request
        title_line_number = request.form["title_line_number"]
        data_first_line_number = request.form["data_first_line_number"]
        data_last_line_number = request.form["data_last_line_number"]
        separator = request.form["separator"]
        data_prefix = request.form["data_prefix"]
        predicate_prefix = request.form["predicate_prefix"]
        input_file = request.form["input_file"]
        output_file = request.form["output_file"]
        # generating the output filename from the input one (test1.csv -> test1.ttl)
        if output_file == "Automatic":
            filename, _ = splitext(input_file)
            output_file = filename + ".ttl"

        # Triplifying and fetching result
        success, message = utils.triplify(title_line_number, data_first_line_number, data_last_line_number, separator,
                                          data_prefix, predicate_prefix, input_file, output_file)

        # loading files contents for preview
        input_file_content = utils.get_file_content(input_file)
        output_file_content = utils.get_file_content(output_file)

    # fetching the existing files from the "/files" directory
    input_files, output_files = utils.get_available_files()
    # If selected, this option will automatically create or select a file with the same name as the input file
    output_files.insert(0, "Automatic")  # put in first position so it is selected by default

    # compute and return the page html code
    return render_template('index.html',
                           title_line_number=title_line_number,
                           data_first_line_number=data_first_line_number,
                           data_last_line_number=data_last_line_number,
                           separator=separator,
                           data_prefix=data_prefix,
                           predicate_prefix=predicate_prefix,
                           input_files=input_files,
                           output_files=output_files,
                           selected_input_file=input_file,
                           selected_output_file=output_file,
                           input_file_content=input_file_content,
                           output_file_content=output_file_content,
                           success=success,
                           message=message)


if __name__ == '__main__':
    from waitress import serve
    print('Launching application on http://localhost:8080/', file=sys.stdout)
    serve(app, host="0.0.0.0", port=8080)
