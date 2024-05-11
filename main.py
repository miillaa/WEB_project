from PIL import Image

from emotion_html import emotion_html
import base64
from flask import Flask, render_template, request, redirect, abort
from data import db_session
from data.users import User
from data.news import News, NewsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route("/home")
def home():
    return render_template("home.html")


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


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    db_sess = db_session.create_session()
    news_item = db_sess.query(News).filter_by(user_id=current_user.id).first()
    with open('temp_image.png', 'rb') as image_file:
        binary_data = image_file.read()
        image = base64.b64encode(binary_data).decode('utf-8')
    if news_item:
        news_item.image = image
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.image = image
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')

    db_sess.commit()
    return render_template('news.html', title='Новости', form=form, news=news_item, image=image)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            image = news.image
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            image = news.image
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Новости', form=form, news=news, image=image)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    img = Image.open('static/body.jpg')
    img.save('temp_image.png')
    return redirect("/")


@app.route('/save_image', methods=['POST'])
@login_required
def save_image():
    data = request.json
    if 'image' in data:
        image_data = data['image']
        _, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)

        with open('temp_image.png', 'wb') as f:
            f.write(image_bytes)
    return redirect('/news')


@app.route('/body_mapping/<feeling1>,<feeling2>,<feeling3>')
@login_required
def body_mapping(feeling1, feeling2, feeling3):
    if request.method == 'GET':
        return render_template('body_mapping.html', param1=feeling1.capitalize(), param2=feeling2.capitalize(),
                               param3=feeling3.capitalize())


@app.route('/emotions', methods=['POST', 'GET'])
@login_required
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
