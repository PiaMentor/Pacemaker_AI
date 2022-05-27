import os
import cv2
from time import sleep
from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import Form
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask('PIA Week 5')
app.config['UPLOAD_FOLDER'] = 'static'
app.config['SECRET_KEY'] = 'Do your best!'

class ReusableForm(Form):
    pass


@app.route('/')
def index():
    return 'Hello'


@app.route('/test/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"./{app.config['UPLOAD_FOLDER']}/{filename}")
            return redirect(url_for('analyze', filename=filename))
    return '''
    <!doctype html>
    <title>Test</title>
    <h1>Upload a test file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/analyze/<filename>')
def analyze(filename):
    image = cv2.imread(f"./{app.config['UPLOAD_FOLDER']}/{filename}")
    height, width, depth = image.shape
    label = predict(image)

    return f'''<html>
    <body>
    <img src="{url_for(app.config['UPLOAD_FOLDER'], filename=filename)}" alt="test image">
    <br>
    <br>
    Image Size: {width} x {height}
    <br>
    Prediction: {label}
    </body>
    </html>    
    '''


def predict(image):
    # import joblib
    # model = joblib.load(model_filename)
    #feature = get_feature(image)
    #ret = model.predict(feature)
    return 'Hard to tell!'


@app.route('/label/<filename>', methods=['GET', 'POST'])
def label(filename):
    form = ReusableForm()

    if request.method == 'POST':
        session.pop('_flashes', None)

        if request.form.get('action') == 'Cat':
            flash(f'{filename} is a cat')
            
            return redirect(url_for('label', filename=filename))

        elif request.form.get('action') == 'Dog':
            flash(f'{filename} is a dog')
            
            return redirect(url_for('label', filename=filename))

    return render_template('label.html', form=form, filename=url_for(app.config['UPLOAD_FOLDER'], filename=filename))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
