from flask import Flask, jsonify,request
import os
import time

UPLOAD_FOLDER = 'static/uploads'

app =Flask(__name__)
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
 def home():
   return 'File Upload Demo'









@app.route('/uploadfile', methods=['GET','POST'])
def uploadfile():
    if request.method == 'POST':
        foto = request.files['foto']
        if foto:

            timestamp = str (int(time.time()))

            ext = foto.filename.split('.')[-1]

            unique_filename = f "{timestamp}.{ext}"

            foto
