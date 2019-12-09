"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import cv2
import numpy as np
import base64
import sys
import os.path
from datetime import datetime
from matplotlib import pyplot as plt
from cmnd_to_text import *
from detect_back_side import *
from flask import Flask,request,send_file,render_template,jsonify
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
lastss=''
currss=''
ocr_result=''
dir_path='C:/temp_data/'
finger_result=''

def server_init():
    ssid = open(dir_path+'session.id', 'r')
    lastssid = ssid.readline().rstrip('\n')
    return lastssid
def write_session(session):
    with open(dir_path+'session.id', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(session.rstrip('\r\n') + '\n' + content)
    return True

@app.route('/')
def hello():
    global lastss
    """Renders a sample page."""
    lastss=server_init()
    #app_init()
    return 'This session: ' + lastss

@app.route('/app_connect', methods=['GET'])
def app_init():
    global currss
    now = datetime.now()
    newssid = now.strftime("%d%m%y%H%M%S%f")
    currss= newssid
    write_session(newssid)
    return jsonify(
    ssid=currss+'-'+lastss)

@app.route('/app_upload_front', methods=['POST'])
def app_upload_front():
    global ocr_result
    try :
        filestr = request.files['image'].read()
        npimg = np.fromstring(filestr, np.uint8)
        # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan
        img1 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)         
        text_img=crop_face_and_text_line(img1)[1]
        face_img=crop_face_and_text_line(img1)[0]
        if len(text_img)<300:
            return jsonify(
            error='null')
        else:
            cv2.imwrite(dir_path+currss+'textimg.jpg', text_img)
            cv2.imwrite(dir_path+currss+'faceimg.jpg', face_img)
            result=IDcard_ocr(text_img)        
            ocr_result = jsonify(
            idn=result[0].rstrip().replace("\n"," "),
            _idn='',
            name=result[2].rstrip().replace("\n"," "),
            _name='',
            birth=result[1].rstrip().replace("\n"," "),
            _birth='',
            place=result[4].rstrip().replace("\n"," "),
            _place='',
            hometown=result[3].rstrip().replace("\n"," "),
            _hometown=''
            )
    except Exception as e:
        return jsonify(
        error=str(e))
    else:
        return jsonify(
        stt='Done')
@app.route('/app_upload_back', methods=['POST'])
def app_upload_back():
    global currss
    try :
        filestr = request.files['image'].read()
        npimg = np.fromstring(filestr, np.uint8)
        # Chuyen doi du lieu numpy array ve du lieu ma tran anh chuan
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR) 
        cv2.imwrite(dir_path+currss+'back.jpg', img)
        result=detect_back_side_ID(img)
        result=cv2.rotate(result, cv2.ROTATE_90_COUNTERCLOCKWISE)
    except Exception as e:
        return jsonify(
        error=str(e))
    else:          
        if len(result)<200:
            return jsonify(
            error='null')
        else:
            cv2.imwrite(dir_path+currss+'finger.jpg', result)
            return jsonify(
            stt='Done')


@app.route('/app_ocr_result', methods=['GET'])
def app_ocr_result():
    #result=idcard_OCR(img)
    return ocr_result
if __name__ == '__main__':
    import os
    HOST = '0.0.0.0'
    try:
        PORT = int(os.environ.get('SERVER_PORT', '56789'))
        lastss=server_init()
    except ValueError:
        PORT = 56789
        lastss=server_init()
    app.run(HOST, PORT)
