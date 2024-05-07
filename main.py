import os

from flask import Flask, render_template, send_file, request, jsonify, redirect
from PIL import Image
from emotion_html import emotion_html

import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
    print(data)
    if 'image' in data:
        image_data = data['image']
        _, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        with open('temp_image.png', 'wb') as f:
            f.write(image_bytes)

        img = Image.open('temp_image.png')
        img.show()
        return 'Изображение получено и отображено'
    else:
        return 'Ошибка: Не удалось получить изображение'


@app.route('/body_mapping/<feeling1>,<feeling2>,<feeling3>')
def body_mapping(feeling1, feeling2, feeling3):
    if request.method == 'GET':
        return render_template('try8_working.html', param1=feeling1.capitalize(), param2=feeling2.capitalize(),
                               param3=feeling3.capitalize())


@app.route('/emotions', methods=['POST', 'GET'])
def emotions():
    if request.method == 'GET':
        return emotion_html()
    elif request.method == 'POST':
        result = []
        for i in request.form:
            result.append(request.form.get(i, ''))
        if len(result) == 3:
            return redirect(f'/body_mapping/{result[0]},{result[1]},{result[2]}')
        else:
            return "Choose 3 emotions"


if __name__ == '__main__':
    app.run(debug=True)
