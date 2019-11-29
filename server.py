from flask import Flask, request, Response
from flask_cors import CORS
import os
import json
import csv
import uuid
app = Flask(__name__)
CORS(app)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
FIELD_NAMES = ['id', 'question', 'option_1',
               'option_2', 'option_3', 'option_4', 'answer']


def _generate_id():
    return str(uuid.uuid4())[:8]


def _read_csv():
    with open(FILE_PATH + '/questions/questions.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return(list(csv_reader))


def _write_to_csv(data):
    existing_data = _read_csv()
    data['id'] = _generate_id()
    existing_data.append(data)
    with open(FILE_PATH + '/questions/questions.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
        csv_writer.writeheader()
        csv_writer.writerows(existing_data)


@app.route("/questions")
def serve_questions():
    data = _read_csv()
    return Response(json.dumps(data), status=200)


@app.route("/add", methods=['POST'])
def add_questions():
    data = request.json
    _write_to_csv(data)
    return Response(status=200)


if __name__ == '__main__':
    app.run()
