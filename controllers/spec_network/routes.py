from flask import session, redirect, url_for, render_template, request
from .forms import LoginForm

from jinja2 import TemplateNotFound
import config
import os, time, cv2
from flask_restplus import Api, Resource, Namespace

import numpy as np

from . import mod


@mod.route('/log', methods=['GET'])
def get_log():
    return render_template('stream_log.html')


@mod.route('/stream_log')
def stream():
    def generate():
        with open('logs/python.log') as f:
            while True:
                yield f.read()
                time.sleep(1)

    return mod.response_class(generate(), mimetype='text/plain')


@mod.route("/room", methods=['POST', 'GET'])
def verify():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '') or "name"
        form.room.data = session.get('room', '') or "room"
    return render_template('room.html', form=form)


@mod.route("/index", methods=['POST', 'GET'])
def demo():
    name = session.get('name', '') or "demo"
    room = session.get('room', '') or 1
    return render_template('chat_thermo_server.html', name=name, room=room)


@mod.route("/logs", methods=['GET'])
def log():
    return render_template('log.html')

# @mod.route("/register/temperature", methods=['POST', 'GET'])
# def detect_temperature():
#     global temp_detect
#     temp_detect = float(request.form['temp_detect'])
#     return jsonify({"success": True}), 200
