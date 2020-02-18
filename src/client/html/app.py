#-*- coding:utf-8 -*-
import os
import cv2
import sys
from flask import Flask, render_template, Response, redirect, request, url_for, make_response
from client.html.camera import Camera
from client.db import database
from client import config
from client.vision import register as vision_register
from client.vision.cascade import haar
from client.client import Client

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
IMAGES_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'static')
if os.path.exists(IMAGES_DIR_PATH) == False:
    os.mkdir(IMAGES_DIR_PATH)

app = Flask(__name__)
app._static_folder = IMAGES_DIR_PATH


@app.route('/')
def index():
    if Client().is_nasa_running():
        return render_template('index.html', patient_id='-1', error="Wait! NASA Is moving")
    new_patient_id = database.create_new_id()
    return render_template('index.html', patient_id=new_patient_id, error="")


@app.route('/register/<patient_id>', methods=['GET', 'POST'])
def register(patient_id):
    error=""
    if Client().is_nasa_running():
        return redirect(url_for('index'))

    if request.method =="POST":
        patient_id = request.form["patient_id"]
        name = request.form["name"]
        age = request.form["age"]
        medicine1 = request.form["medicine1"]
        medicine2 = request.form["medicine2"]
        medicine3 = request.form["medicine3"]
        if name == "" or age == "" or medicine1 =="" or medicine2=="" or medicine3=="":
            error = "Error! Blank Found"
            return make_response(render_template('register.html', patient_id=patient_id, error=error))
        elif age.isdigit() == False or medicine1.isdigit() == False or \
            medicine2.isdigit() == False or medicine3.isdigit() == False:
            error = "Error! int : age, medicine1, medicine2, medicine3 "
            return make_response(render_template('register.html', patient_id=patient_id, error=error))
        patient_info = {
            "id" : patient_id,
            "name" : name,
            "age" : age
        }
        medicine_info = {
            "id" : patient_id,
            "medicine1" : medicine1,
            "medicine2" : medicine2,
            "medicine3" : medicine3
        }
        if database.save_patient_info(patient_id, patient_info) and \
            database.save_medicine_info(patient_id, medicine_info):
            if vision_register.train(patient_id, os.path.join(IMAGES_DIR_PATH, patient_id)):
                return redirect(url_for('index'))
            else:
                error = "Error No Face Found"
                database.delete_medicine_info(patient_id)
                database.delete_patient_info(patient_id)
        else:
            error = "Error Update Database Failed"
    PATIENT_IMAGE_DIR_PATH = os.path.join(IMAGES_DIR_PATH, patient_id)
    if os.path.exists(PATIENT_IMAGE_DIR_PATH) == False:
        os.mkdir(PATIENT_IMAGE_DIR_PATH)
    if database.has_patient_id(patient_id):
        return redirect(url_for('index'))
    return render_template('register.html', patient_id=patient_id, error=error)


def gen(camera):
    while True:
        frame = camera.get_frame()
        #frame = haar.draw_rectangle_on_face(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    if Client().is_nasa_running():
        return redirect(url_for('index'))
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture/<patient_id>')
def capture(patient_id):
    if Client().is_nasa_running():
        return redirect(url_for('index'))
    captured_img = Camera.capture()
    file_name = '{}.jpg'.format(database.create_random_string(config.TEMP_IMAGE_FILE_NAME_LENGTH))
    if captured_img == None:
        return 'fail'

    PATIENT_IMAGE_DIR_PATH = os.path.join(IMAGES_DIR_PATH, patient_id)
    if os.path.exists(PATIENT_IMAGE_DIR_PATH) == False:
        os.mkdir(PATIENT_IMAGE_DIR_PATH)
    file_path = os.path.join(PATIENT_IMAGE_DIR_PATH, file_name)
    with open(file_path, 'wb') as fd:
        fd.write(captured_img)
    return os.path.join(os.path.join('/static', patient_id), file_name)