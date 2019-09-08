import json

import redis
from flask import abort, Flask, jsonify, request
from flask_cors import CORS, cross_origin
from structlog import get_logger

from src.payload import make_payload

app = Flask(__name__)
CORS(app, allow_headers='Content-Type')
redis_app = redis.Redis(host='redis', port=6379)
log = get_logger()
FRONTEND_URL = 'https://cisco-manager.priv.hackademint.org'


@app.route('/update', methods=['GET'])
@cross_origin(origins=FRONTEND_URL)
def update():
    response = redis_app.xread(streams={'update': 0}, count=1)
    if not response:
        abort(404)
    msg_id = response[0][1][0][0]
    message = response[0][1][0][1][b'message']
    redis_app.xdel('update', msg_id)
    return jsonify(dict(id=msg_id.decode(), message=message.decode()))


@app.route('/config', methods=['GET'])
def config():
    response = redis_app.get('config_cisco')
    if response is None:
        abort(404)
    response = json.loads(response)
    result = dict(message=response['json'], time=response['time'])
    return jsonify(result)


@app.route('/action', methods=['POST'])
@cross_origin(origins=FRONTEND_URL)
def store():
    if not request.form:
        abort(404)

    data = dict(request.form)
    content = make_payload(data)
    if content is None:
        abort(404)

    redis_app.xadd('todo', {'json': content})
    log.info('Storing data', stream='todo', field='json', content=content)
    return jsonify(data), 200


if __name__ == '__main__':
    content = json.dumps({'type': 'update'})
    redis_app.xadd('todo', {'json': content})
    log.info('Storing data', stream='todo', field='json', content=content)
    app.run(port=80, debug=True)
