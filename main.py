import os

from flask import Flask, render_template, send_file, request, jsonify, redirect
from emotion_html import emotion_html

import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/body_mapping/<feeling1>,<feeling2>,<feeling3>', methods=['POST', 'GET'])
def body_mapping(feeling1, feeling2, feeling3):
    if request.method == 'GET':
        return render_template('body_mapping.html', param1=feeling1.capitalize(), param2=feeling2.capitalize(),
                               param3=feeling3.capitalize())
    elif request.method == 'POST':
        return jsonify({'message': 'Image saved successfully'}), 200


@app.route('/emotions', methods=['POST', 'GET'])
def emotions():
    if request.method == 'GET':
        return emotion_html()
    elif request.method == 'POST':
        print(request.form)
        result = []
        for i in request.form:
            result.append(request.form.get(i, ''))
        if len(result) >= 3:
            return redirect(f'/body_mapping/{result[0]},{result[1]},{result[2]}')
        else:
            return "Choose 3 emotions"


if __name__ == '__main__':
    app.run(debug=True)