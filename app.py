import datetime
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from flask import Flask, render_template, g, request, flash, url_for,redirect,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import psycopg2
from FDataBase import FDataBase
# postgresql
import psycopg2
import psycopg2.extras
import hashlib
from config import host, db_name, user, password
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# для  flash
SECRET_KEY = 'dhjdkjnfuefjkdsnfsdjfds'
app.config['SECRET_KEY'] = 'FHSGGSDBGDRUIDNGHDYHFDGJKFDJHBF'


login_manager = LoginManager(app)
"""если пользователь не имеет доступ к странице сайта,его перекидывает на авторизацию"""
login_manager.login_view = 'login'
login_manager.login_message = "Aвторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = 'success'

@login_manager.user_loader
def load_user(user_id):
    print('load user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    connection = psycopg2.connect(host=host, user=user, password=password,
                                  database=db_name)
    connection.autocommit = True

    return connection


def get_db():
    # установка соединения
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    # разрыв соединения
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    """Устанавливаем соединение с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/')
@login_required
def index():
    return render_template("base.html")




@app.route("/add_product", methods=['POST', 'GET'])
@login_required
def addProduct():
    if request.method == "POST":
        name = request.form.get('name')
        price = request.form.get('price')
        discounted_price = request.form.get('discounted_price')
        print(name, price, discounted_price)
        if price and name and discounted_price is not None:
            res = dbase.addProduct(name, price, discounted_price)
            if not res:
                flash("Ошибка добавления статьи", category='error')
            else:
                flash('Cтатья добавлена успешно', category="success")
        # else:
        #     if len(request.form['name']) > 4 and len(request.form['post']) > 10 and len(
        #             request.form['language']) > 2 and len(request.form['url']) > 2:
        #         url = request.form['url']
        #         res = dbase.addProduct(request.form['name'], request.form['post'], url[:5],
        #                             request.form['language'], author)
        #         if not res:
        #             flash("Ошибка добавления статьи", category='error')
        #         else:
        #             flash('Cтатья добавлена успешно', category="success")
        #     else:
        #         flash("Ошибка добавления статьи2", category='error')

    return render_template("add.html")


@app.route("/add_card", methods=['POST', 'GET'])
@login_required
def addСard():
    if request.method == "POST":
        name = request.form.get('card_series')
        price = request.form.get('card_number')
        discounted_price = request.form.get('card_status')
        dis = request.form.get('current_discount')
        author = current_user.getName()
        if len(request.form['card_series']) > 1:
            res = dbase.addСard(request.form['card_series'],
                                request.form['card_number'],
                                request.form['language'],
                                request.form['current_discount'],request.form['end_card'],author)
            if not res:
                flash("Ошибка добавления карты", category='error')
            else:
                flash('Cтатья добавлена успешно', category="success")
        else:
            flash("Данные введены не корректно", category='error')

    return render_template("add_card.html")


@app.route("/generate_card", methods=['POST', 'GET'])
@login_required
def addRandomСard():
    if request.method == "POST":
        card_series = request.form.get('card_series')
        count = request.form.get('count')
        card_status = request.form.get('language')
        current_discount = request.form.get('current_discount')
        end_card = request.form.get('end_card')
        author = current_user.getName()
        print(count)
        while int(count) != 0:
            card_number = 0
            count = int(count) -1
            card_number = random.randint(10000000, 99999999)
            res = dbase.addСard(card_series,card_number,card_status,current_discount,end_card,author)
            if not res:
                flash("Ошибка создания карты", category='error')
            else:
                flash('Карта добавлена успешно', category="success")
            continue

        # if len(request.form['card_series']) > 1:
        #     res = dbase.addСard(request.form['card_series'],
        #                         request.form['card_number'],
        #                         request.form['language'],
        #                         request.form['current_discount'],request.form['end_card'],author)
        #     if not res:
        #         flash("Ошибка добавления карты", category='error')
        #     else:
        #         flash('Cтатья добавлена успешно', category="success")
        # else:
        #     flash("Данные введены не корректно", category='error')

    return render_template("random_generate.html")

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    # если данные были отправлены и введены корректно
    if form.validate_on_submit():
        user = dbase.getUserByName(form.name.data)
        hash = hashlib.md5(bytes(form.psw.data, encoding='utf-8'))
        print(hash.hexdigest())
        # if user and check_password_hash(user['psw'], form.psw.data):
        if user and user['psw'] == hash.hexdigest():
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html",  form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    csrf_token = request.args.get('csrf_token')
    name = request.args.get('name')
    email = request.args.get('email')
    psw = request.args.get('psw')
    psw2 = request.args.get('psw2')
    submit = request.args.get('submit')
    print(csrf_token, name, email, psw, psw2, submit)
    if csrf_token and name and email and psw and psw2 and submit is not None and psw == psw2:

        hash = hashlib.md5(bytes(psw, encoding='utf-8'))
        res = dbase.addUser(name, email, hash.hexdigest())
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            hash = hashlib.md5(bytes(form.psw.data, encoding='utf-8'))
            print(f'Password ' + hash.hexdigest())
            # hash = generate_password_hash(form.psw.data)
            res = dbase.addUser(form.name.data, form.email.data,
                                hash.hexdigest())
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")

    return render_template("register.html",form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    if db:
        try:
            card=[]
            author = current_user.getName()
            card = dbase.getCardsByName(author)
            if card:
                flash("Карты успешно загружены", "success")
                # return redirect(url_for('or'))
            else:
                flash("Ошибка при загрузке из БД", "error")
            # cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            # cur.execute(
            #     f"SELECT card_series, card_number,data_card_create,data_card_end,data_card_last_use,total_sum,card_status,current_discount FROM Cards ORDER BY card_series DESC")
            # list = cur.fetchall()
            # print(list)

        except Exception as e:
            print("Ошибка получения статей из БД " + str(e))
    return render_template('profile.html',card=card)

@app.route("/card/<alias>")
@login_required
def ShowPost(alias):
    res = dbase.getCard(alias)
    if not res["owner"]:
        abort(404)
    return render_template('card.html',  card_series=res["card_series"], card_number=res["card_number"], data_card_create=res["data_card_create"], owner=res["owner"],
                           current_discount=res["current_discount"],data_card_end=res["data_card_end"],data_card_last_use=res["data_card_last_use"],
                           total_sum=res["total_sum"],card_status=res["card_status"])



if __name__ == "__main__":
    app.run(debug=True)
