from flask import Flask, request, json
import entities


app = Flask(__name__)


def json_response(data, status=200):
    return json.dumps(data), status, {'Content-Type': 'application/json'}


@app.route('/')
def app_works():
    return json_response("server works")


@app.route('/test_results', methods=['POST'])
def get_bank_approvals():
    dict_from_request = json.loads(request.data)
    return json_response(entities.get_bank_approvals(dict_from_request))


@app.route('/create_bank', methods=['POST'])
def create_bank_demands():
    dict_from_request = json.loads(request.data)
    return json_response(entities.create_bank_demands(dict_from_request))


@app.route('/update_bank', methods=['POST'])
def update_bank_demands():
    dict_from_request = json.loads(request.data)
    return json_response(entities.update_bank_demands(dict_from_request))


@app.route('/delete_bank', methods=['POST'])
def delete_bank():
    dict_from_request = json.loads(request.data)
    return json_response(entities.delete_bank_demands(dict_from_request))


@app.route('/get_bank_names', methods=['GET'])
def get_bank_names():
    return json_response(entities.get_all_bank_names())


# app.run()
