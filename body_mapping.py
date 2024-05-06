import os

from flask import Flask, render_template, send_file, request, jsonify
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/body_mapping/<feeling1>,<feeling2>,<feeling3>', methods=['POST', 'GET'])
def index(feeling1, feeling2, feeling3):
    if request.method == 'GET':
        return render_template('body_mapping.html', param1=feeling1.capitalize(), param2=feeling2.capitalize(),
                               param3=feeling3.capitalize())
    elif request.method == 'POST':
        return jsonify({'message': 'Image saved successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
