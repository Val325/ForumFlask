from flask import Flask, redirect
from flask import render_template, current_app
from flask import request, session
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine  
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String
from sqlalchemy import select
from flask_bcrypt import Bcrypt
import os
from DB import Database, Text, Users
from flask import Blueprint
from config import UPLOADS_PATH, ALLOWED_EXTENSIONS

app = Flask(__name__)

utils = Blueprint('utils', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_file(request):
    filename = ''
    image_src = ''
    file = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #image_src = app.config['UPLOAD_FOLDER'] + filename
            file.save(os.path.join(UPLOADS_PATH, filename))
            image_src = UPLOADS_PATH + filename

        
        
        full_filename = os.path.join(os.path.join('uploads'), filename)

        filedata = {
            "filename": filename,
            "full_filename": full_filename,
            "source": image_src, 
            "file": file
        }
        return filedata