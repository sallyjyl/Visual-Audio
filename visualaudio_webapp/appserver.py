# python3 appserver.py
#
# For own machine
# 127.0.0.1:5000
#
# For another device connected to same LAN
# Go to <server IP address>:5000

import os
import flask
#import time
import mimetypes
import uuid
import io

from werkzeug.utils import secure_filename

#from pygame import mixer

import computer
import storage

#UPLOAD_FOLDER = 'text_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = flask.Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(16)

@app.route('/')
def root():
    #print ('ip ' + flask.request.remote_addr)
    return flask.redirect(flask.url_for('uploads'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    audio_filename = None
    url_and_keyword = []

    if flask.request.method == 'POST':
        print (flask.request)
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)# + str(time.time())
            #print('file: ' + filename)
            #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #if not os.path.exists(app.config['UPLOAD_FOLDER']):
            #    os.makedirs(app.config['UPLOAD_FOLDER'])
            #file.save(filepath)
            url_and_keyword, voice_audio = computer.final_audio_from_image(file, filename=filename)
            #        filepath, filename+'.mp3')
            #        file, filename+'.mp3')

            #mixer.init()
            #mixer.music.load(filename+'.mp3')
            #mixer.music.play()

            if 'user' not in flask.session:
                flask.session['user'] = str(uuid.uuid4())

            audio_filename = filename +'.mp3'
            storage.upload_data(flask.session['user'] + '/' + audio_filename,
                voice_audio)

            for (url, keyword) in url_and_keyword:
                print (url +' ' + keyword)

    return flask.render_template('upload.html', 
        audiofile=audio_filename, url_keyword=url_and_keyword)

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/text_sound/<path:filename>')
def sound_file(filename):
    if 'user' not in flask.session:
        flask.session['user'] = str(uuid.uuid4())

    filepath = flask.session['user'] + '/' + filename
    #with open(filename, 'rb') as f:
    #    data = f.read()
    data = storage.download_data(filepath)

    #file_mimetype = mimetypes.guess_type(filename)[0] \
    #        or 'application/octet-stream'
    #os.remove(filename)
    #delete(filename)

    return flask.send_file(io.BytesIO(data), attachment_filename=filename)

    #return flask.send_from_directory('./', filename)

@app.route('/VisualAudio.jpg')
def vis_audio():
    return flask.send_from_directory('./', 'VisualAudio.jpg')

if __name__ == '__main__':
    #app.run()
    #app.debug = True
    app.run(host = '0.0.0.0',port=5000)