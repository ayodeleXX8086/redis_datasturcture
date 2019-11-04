from cache_data_structure.LRUCache import CacheClient,DataNotFoundException,CacheClientNotFoundException
from cache_server.get_input_args import get_input_args
from flask import Flask,jsonify,request

import json
import threading

app = Flask(__name__)
'''
This is used to update the cache when data is needed to be evicted
'''
updater = threading.Thread()


@app.before_first_request
def cache_updater():
    global updater
    if not updater.isAlive():
        updater = CacheClient.updater_thread()
        updater.start()


@app.route('/cache_service/sub',methods=['GET'])
def sub_data():
    try:
        data     = CacheClient.remove_header()
        return jsonify(data)
    except CacheClientNotFoundException:
        return client_does_not_exist()
    except DataNotFoundException:
        return sub_data_not_found()

@app.route('/cache_service/<key>',methods=['GET'])
def find_data(key):
    try:
        return jsonify(CacheClient.get_data(key))
    except DataNotFoundException:
        return data_not_found(key)
    except CacheClientNotFoundException:
        return client_does_not_exist()

@app.route("/cache_service",methods=['POST','PUT'])
def save_or_update_data():
    """
    Json request sample
    {'key':'google.com',value:[1,2,3,4]}
    :return:
    """
    try:
        req_data = json.loads(request.data)
        CacheClient.set_data(req_data['key'],req_data['value'])
        response = jsonify({"message":"success"})
        return response
    except CacheClientNotFoundException:
        return client_does_not_exist()


@app.errorhandler(400)
def data_not_found(key):
    message = {
        'message': f'The {key} cannot be found in the cache'
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

@app.errorhandler(400)
def sub_data_not_found():
    message = {
        'message': f'There is no data in the cache '
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

@app.errorhandler(500)
def client_does_not_exist():
    message = {
        'message': 'The client as not been setup properly'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp





if __name__ == '__main__':
    arguments = get_input_args()
    CacheClient.create_client(arguments.strategy,arguments.threshold)
    app.run(debug=True)




