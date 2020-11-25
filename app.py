import importlib, os, sys, time, cv2, base64, traceback, json, _thread
from time import sleep
from datetime import datetime
import numpy as np
from multiprocessing import Process, Manager
from flask import Flask, render_template
from engineio.payload import Payload
from flask_socketio import SocketIO
from flask_restplus import Api, Resource, fields
import logging.config
import config
from flask import session
from flask_socketio import emit, join_room, leave_room
import base64
import json

log_config_dir = 'config/logging.conf'
logging.config.fileConfig(log_config_dir, disable_existing_loggers=False)

Payload.max_decode_packets = 500
app = Flask(__name__)
api = Api(app)
app.config.from_object(config.Config)
center_socketio = SocketIO()
center_socketio.init_app(app)
ROOMS = {'1': {'status': 'active'}}
number_of_detected_person = {}

### FOR FLASK BLUE PRINT
def register_all_module_controller():
    d = './controllers'
    list_dir = [o for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    print(list_dir)
    for module in list_dir:
        module_page = importlib.import_module('controllers.' + str(module))
        app.register_blueprint(module_page.mod)


def register_module(module_name, url_prefix=None):
    module_page = importlib.import_module('controllers.' + str(module_name))
    if url_prefix is None:
        app.register_blueprint(module_page.mod)
    else:
        app.register_blueprint(module_page.mod, url_prefix=url_prefix)


def register_namespace(api, namespace_name, path=None):
    module_page = importlib.import_module('controllers.' + str(namespace_name))
    if path is None:
        api.add_namespace(module_page.namespace)
    else:
        api.add_namespace(module_page.namespace, path=path)


@center_socketio.on('make_connect', namespace='/thermoai')  # global namespace
def make_connect(message):
    center_socketio.emit('logs', {'msg': 'someone make connection'}, broadcast=True, namespace='/thermoai')
    center_socketio.emit('logs', {'msg': message}, broadcast=True, namespace='/thermoai')


#### Connection : Thermo Ai <=> Central Server
@center_socketio.on('status', namespace='/thermoai')  # global namespace
def make_status(message):
    if type(message) is str:
        message = json.loads(message)
    logging.info(str({'msg': 'someone update status'}))
    logging.info(str({'msg': str(message)}))
    thermo_id = str(message['id'])
    thermo_status = str(message['status'])
    if not ROOMS.get(thermo_id):
        ROOMS[thermo_id] = {'status': thermo_status}
    else:
        ROOMS[thermo_id]['status'] = thermo_status
    center_socketio.emit('logs', {'msg': thermo_id + 'has updated this status to ' + thermo_status}, broadcast=True,
                         namespace='/thermoai')
    center_socketio.emit('logs', {'msg': str(message)}, broadcast=True, namespace='/thermoai')


@center_socketio.on('image_frame', namespace='/thermoai')  # global namespace
def make_image_frame(message):
    if type(message) is str:
        message = json.loads(message)
    # logging.info(str({'msg': str(message)}))
    # print(str({'msg': str(message)}))
    center_socketio.emit('logs', {'msg': str(message['id']) + ' someone center_socketio.emit an image frame'},
                         broadcast=True,
                         namespace='/thermoai')
    room_id = str(message['id'])
    room_name = "thermoai_[" + str(room_id) + "]"
    image = message['image_frame']
    logging.info(str({'msg': 'someone emit an image frame to room: ' + room_name}))
    center_socketio.emit('image_frame', image, broadcast=True, room=room_name, namespace='/monitor')


@center_socketio.on('number_of_detected_person', namespace='/thermoai')  # global namespace
def make_number_of_detected_person(message):
    if type(message) is str:
        message = json.loads(message)
    logging.info(str({'msg': 'someone center_socketio.emit number of detected person'}))
    logging.info(str({'msg': str(message)}))
    thermo_id = str(message['id'])
    thermo_num = message['num']
    if not number_of_detected_person.get(thermo_id):
        number_of_detected_person[thermo_id] = {'num': thermo_num}
    else:
        number_of_detected_person[thermo_id]['num'] = thermo_num
    center_socketio.emit('logs', {'msg': 'someone center_socketio.emit number of detected person'}, broadcast=True,
                         namespace='/thermoai')
    center_socketio.emit('logs', {'msg': str(message)}, broadcast=True, namespace='/thermoai')
    center_socketio.emit('total_num', {'num': thermo_num}, broadcast=True, namespace='/monitor')


@center_socketio.on('detect_high_fever', namespace='/thermoai')  # global namespace
def make_detect_high_fever(message):
    if type(message) is str:
        message = json.loads(message)
    logging.info(str({'msg': 'someone send detected high fever person image'}))
    logging.info(str({'msg': str(message)}))
    center_socketio.emit('logs', {'msg': 'someone send detected high fever person image'}, broadcast=True,
                         namespace='/thermoai')
    center_socketio.emit('logs', {'msg': str(message)}, broadcast=True, namespace='/thermoai')
    room_id = str(message['id'])
    room_name = "thermoai_[" + str(room_id) + "]"
    image = message['image']
    temp = message['temp']
    center_socketio.emit('detect_high_fever', {'id': room_id, 'image': image, 'temp': temp}, broadcast=True,
                         room=room_name, namespace='/monitor')


#### Connection : Monitor App <=> Central Server
@center_socketio.on('thermoai', namespace='/monitor')  # global namespace
def check_thermo_ai_status(message):
    if type(message) is str:
        message = json.loads(message)
    logging.info(str({'msg': str(message)}))
    center_socketio.emit('logs', {'msg': 'someone want to get thermo ai status and streaming url'}, broadcast=True,
                         namespace='/thermoai')

    thermo_id = str(message['id'])
    if ROOMS.get(thermo_id):
        thermo_status = ROOMS[thermo_id]['status']
        stream_url = 'http://35.213.153.96:5009/image_frame?room=' + str(thermo_id)
        center_socketio.emit('logs',
                             {'msg': str({"id": message['id'], 'stream_url': stream_url, "status": thermo_status})},
                             broadcast=True, namespace='/thermoai')
        emit('thermoai', {"id": message['id'], "stream_url": stream_url, "status": thermo_status})
    else:
        emit('thermoai', {"id": message['id'], "stream_url": "", "status": "error"})


@center_socketio.on('thermoai_view', namespace='/monitor')
def on_join(message):
    if type(message) is str:
        message = json.loads(message)
        center_socketio.emit('logs', {"msg": "1 User" + " has send a String." + str(message)}, broadcast=True,
                             namespace='/thermoai')
    room = "thermoai_[" + str(message["id"]) + "]"
    center_socketio.emit('logs', {"msg": "1 User" + " has joined the " + room + " room."}, broadcast=True,
                         namespace='/thermoai')
    join_room(room)


@center_socketio.on('disconnect', namespace='/monitor')
def on_leave(message):
    if type(message) is str:
        message = json.loads(message)
    room = "thermoai_[" + str(message["id"]) + "]"
    leave_room(room)
    center_socketio.emit('logs', {'msg': "1 User" + " has left the room: " + room + "."}, broadcast=True,
                         namespace='/thermoai')


@center_socketio.on('high_fever_list', namespace='/monitor')  # global namespace
def make_status(message):
    if type(message) is str:
        message = json.loads(message)
    logging.info(str({'msg': str(message)}))
    center_socketio.emit('logs', {'msg': 'someone want to get get list of high fever'}, broadcast=True,
                         namespace='/thermoai')
    center_socketio.emit('logs', {'msg': str(message)}, broadcast=True, namespace='/thermoai')

    emit('high_fever_list', {'msg': number_of_detected_person})


from concurrent.futures import ThreadPoolExecutor
from socketIO_client import SocketIO, BaseNamespace

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5009  # The port used by the server


# executor = ThreadPoolExecutor(1)


@app.route('/demo_image_frame', methods=['POST'])
def demo_image_frame():
    global play
    play = not play
    return {"ok": "done"}


@app.route('/thermo_ai', methods=['GET'])
def thermo_ai():
    thermo_ai_list = []
    for key in ROOMS.keys():
        if ROOMS[key]['status'] == "active":
            thermo_ai_list.append({"thermoai_id": key, "name": "出入り口{}".format(key)})

    return {"data": thermo_ai_list}


if __name__ == "__main__":
    executor = ThreadPoolExecutor(1)
    register_module('spec_network')
    app.logger.addHandler(logging.handlers)
    center_socketio.run(app, host="0.0.0.0", port=5009, debug=True, log_output=True), ()
