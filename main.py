import os

from flask import Flask, render_template, send_file, request, jsonify, redirect
# from PIL import Image
from emotion_html import emotion_html
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm, LoginForm
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/exit')
@login_required
def exit():
    logout_user()
    return redirect("/home")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
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
        return render_template('body_mapping.html', param1=feeling1.capitalize(), param2=feeling2.capitalize(),
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
    db_session.global_init("db/blogs.db")
    app.run(debug=True)
