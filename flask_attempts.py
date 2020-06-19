from flask import Flask, request, json
import entities
"""Запустив, можно посылать POST запросы к http://127.0.0.1:5000/,
в ответ будет приходить инфа о банках с условиями"""


app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    dict_from_request = json.loads(request.data)
    print(dict_from_request)
    return json_response(entities.get_bank_approvals(dict_from_request))


def json_response(data, status=200):
    return json.dumps(data), status, {'Content-Type': 'application/json'}


app.run()
