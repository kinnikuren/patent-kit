import os
from flask import Flask, url_for
from flask import request
from flask import render_template
from flask import flash, redirect
from flask import send_from_directory
#from markupsafe import escape
from werkzeug.utils import secure_filename

from PIL import Image

import claim_chart_generator as ccg

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#for static files
#url_for('static', filename='style.css')

@app.route('/')
def index():
    return 'Index Page'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file(snippet=None):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            
            flash('No selected file')
            #return 'no selected file'
            return redirect(request.url)
            #return redirect(url_for('upload'))
        if file and allowed_file(file.filename):
            print("FILE TYPE IS:")
            print(type(file))
            filename = secure_filename(file.filename)
            #pass the file here to a function?
            
            snippet = do_something_with_file(file)

            #file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #file.save(file_save_path)

            test_image_path = "./static/output/claim_chart.png"
            test_image = Image.open(test_image_path) 
            
            return render_template('upload.html', snippet=snippet, image=test_image_path)

            #return redirect(url_for('upload_file'), snippet=snippet)
            #return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def do_something_with_file(file_save_path):
    #print(os.path.abspath(file_save_path))
    """
    with open(file_save_path) as file_reader:
        file_string = file_reader.read()
    """
    file_bytes = file_save_path.stream.read()
    print(type(file_bytes))
    print(file_bytes)
    file_string = file_bytes.decode("UTF-8")
    print(type(file_string))
    #print(type(file_string))
    
    #file_object = None
    #file_save_path.save(file_object)
    #print(type(file_object))
    
    
    #first_100 = file_string[:100]

    claims_dict = ccg.create_claims_dict(file_string)
    ccg.generate_claim_chart(claims_dict)

    print(claims_dict)
    return file_string