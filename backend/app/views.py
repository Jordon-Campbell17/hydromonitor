"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

# from crypt import methods
import site 

from app import app, Config, mongo, Mqtt
from flask import render_template, request, jsonify, send_file
from json import dumps, loads 
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone
from os import getcwd
from os.path import join, exists
from time import time, ctime
from math import floor


@app.route('/api/climo/get/<start>/<end>', methods=['GET']) 
def get_all(start, end):
    if request.method == "GET":
        data = mongo.getAllInRange(start, end)
        if data is not None:
            return jsonify({"status": "found", "data": data})
    return jsonify({"status": "not found", "data": []})


@app.route('/api/mmar/temperature/<start>/<end>', methods=['GET']) 
def get_temperature_mmar(start, end):
    if request.method == "GET":
        data = mongo.temperatureMMAR(start, end)
        if data is not None:
            return jsonify({"status": "found", "data": data})
    return jsonify({"status": "not found", "data": []})


@app.route('/api/mmar/humidity/<start>/<end>', methods=['GET']) 
def get_humidity_mmar(start, end):
    if request.method == "GET":
        data = mongo.humidityMMAR(start, end)
        if data is not None:
            return jsonify({"status": "found", "data": data})
    return jsonify({"status": "not found", "data": []})


@app.route('/api/frequency/<variable>/<start>/<end>', methods=['GET']) 
def get_freq_distro(variable, start, end):
    if request.method == "GET":
        data = mongo.frequencyDistro(variable, start, end)
        if data is not None:
            return jsonify({"status": "found", "data": data})
    return jsonify({"status": "not found", "data": []})


@app.route('/api/file/get/<filename>', methods=['GET']) 
def get_images(filename):
    if request.method == "GET":
        file_path = join(getcwd(), Config.UPLOADS_FOLDER, filename)
        if exists(file_path):
            return send_file(file_path)
        return jsonify({"status": "file not found"}), 404


@app.route('/api/file/upload', methods=["POST"])  
def upload():
    if request.method == "POST": 
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(join(getcwd(), Config.UPLOADS_FOLDER, filename))
        return jsonify({"status": "File upload successful", "filename": f"{filename}"})


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(405)
def page_not_found(error):
    return jsonify({"status": 404}), 404