import os
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import similar_sentence as sim

ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'r') as f:
            txt_list = f.readlines()
        text_list = [sim.process_text(text) for text in txt_list]
        text_list = [x for x in text_list if x]
        results = sim.get_similar_pair(text_list)
        resp = jsonify({'similar_pairs': f'{results}'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types is txt'})
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    app.run()
