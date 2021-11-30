import configparser
from os.path import splitext

from flask import Flask, render_template, request

import utils

app = Flask(__name__)

config = configparser.SafeConfigParser()
config.read('defaults.ini')


# TODO improve UI
# TODO add README & comments

@app.route('/', methods=["GET", "POST"])
def index():
    input_files, output_files = utils.get_available_files()
    output_files.append("Automatic")
    if request.method == "GET":
        title_line_number = config.get("DEFAULT", "title")
        data_first_line_number = config.get("DEFAULT", "data")
        data_last_line_number = None
        separator = config.get("DEFAULT", "sep")
        data_prefix = config.get("DEFAULT", "prefix_data")
        predicate_prefix = config.get("DEFAULT", "prefix_predicate")
        input_file = None
        output_file = "Automatic"
        input_file_content = "Launch triplificator to see preview"
        output_file_content = "Launch triplificator to see preview"
    else:
        title_line_number = request.form["title_line_number"]
        data_first_line_number = request.form["data_first_line_number"]
        data_last_line_number = request.form["data_last_line_number"]
        separator = request.form["separator"]
        data_prefix = request.form["data_prefix"]
        predicate_prefix = request.form["predicate_prefix"]
        input_file = request.form["input_file"]
        output_file = request.form["output_file"]
        if output_file == "Automatic":
            filename, _ = splitext(input_file)
            output_file = filename + ".ttl"

        success, message = utils.triplify(title_line_number, data_first_line_number, data_last_line_number, separator,
                                          data_prefix, predicate_prefix, input_file, output_file)
        input_file_content = utils.get_file_content(input_file)
        output_file_content = utils.get_file_content(output_file)
        print(str(success) + message)  # TODO print in UI as a toast

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
                           output_file_content=output_file_content)


if __name__ == '__main__':
    # TODO remove debug mode
    app.run(debug=True)
