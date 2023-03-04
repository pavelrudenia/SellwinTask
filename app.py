import datetime
from flask_login import LoginManager, login_user, login_required, current_user, \
    logout_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from flask import Flask, render_template, g, request, flash, url_for, redirect, \
    abort, jsonify
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
    dbase.UpdateStatus()


@app.route('/')
@login_required
def index():
    return render_template("base.html")

"""http://127.0.0.1:5000/add_product?csrf_token=ImVjZDExOTgzOTE5NzQ5M2YzOWNlZjI4Mjg3MGVmY2NiNzA0MTZhNzIi.YnDP1Q.2zuvpB4hCJYiHd3jCocbxOa-vKk&name=диван&price=300&discounted_price=279"""
@app.route("/add_product", methods=['POST', 'GET'])
@login_required
def addProduct():
    if request.method == "POST":
        name = request.args.get('name')
        price = request.args.get('price')
        discounted_price = request.args.get('discounted_price')

        if name and price and discounted_price  is not None:
            res = dbase.addProduct(name, price, discounted_price)
            if not res:
                flash("Ошибка добавления статьи", category='error')
            else:
                flash('Cтатья добавлена успешно', category="success")
        else:
            name = request.form.get('name')
            price = request.form.get('price')
            discounted_price = request.form.get('discounted_price')
            if price and name and discounted_price is not None:
                res = dbase.addProduct(name, price, discounted_price)
                if not res:
                    flash("Ошибка добавления статьи", category='error')
                else:
                    flash('Cтатья добавлена успешно', category="success")

    return render_template("add.html")


"""http://127.0.0.1:5000/add_card?csrf_token=ImVjZDExOTgzOTE5NzQ5M2YzOWNlZjI4Mjg3MGVmY2NiNzA0MTZhNzIi.YnDP1Q.2zuvpB4hCJYiHd3jCocbxOa-vKk&card_series=AA&card_number=77777777&language=%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%B0%D1%8F&end_card=2023-03-19T22%3A40&current_discount=11&author=pavel"""
@app.route("/add_card", methods=['POST', 'GET'])
@login_required
def addСard():
    if request.method == "POST":
        author = request.args.get('author')
        card_series = request.args.get('card_series')
        card_number = request.args.get('card_number')
        language = request.args.get('language')
        current_discount = request.args.get('current_discount')
        end_card = request.args.get('end_card')
        if card_series and card_number and language and current_discount and end_card is not None:
            res = dbase.addСard(card_series,card_number,language,current_discount,end_card,author)
            if not res:
                flash("Ошибка добавления карты,данный номер уже занят",
                      category='error')
            else:
                flash('Карта добавлена успешно', category="success")
        else:
            if len(request.form['card_series']) > 1:
                res = dbase.addСard(request.form['card_series'].upper(),
                                    request.form['card_number'],
                                    request.form['language'],
                                    request.form['current_discount'],
                                    request.form['end_card'], author)
                if not res:
                    flash("Ошибка добавления карты,данный номер уже занят",
                          category='error')
                else:
                    flash('Карта добавлена успешно', category="success")
            else:
                flash("Данные введены не корректно", category='error')

    return render_template("add_card.html")



"""http://127.0.0.1:5000/generate_card?csrf_token=ImVjZDExOTgzOTE5NzQ5M2YzOWNlZjI4Mjg3MGVmY2NiNzA0MTZhNzIi.YnDP1Q.2zuvpB4hCJYiHd3jCocbxOa-vKk&language=%D0%90%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%B0%D1%8F&card_series=xx&count=1&end_card=2023-03-04T21%3A51&current_discount=64&author=pavel&card_status=Активная"""
@app.route("/generate_card", methods=['POST', 'GET'])
@login_required
def addRandomСard():
    if request.method == "POST":
        author = request.args.get('author')
        card_series = request.args.get('card_series')
        card_status = request.args.get('language')
        current_discount = request.args.get('current_discount')
        end_card = request.args.get('end_card')
        count = request.args.get('count')
        if card_series and card_status and count and current_discount and end_card is not None:
            while int(count) != 0:
                count = int(count) - 1
                card_number = random.randint(10000000, 99999999)
                res = dbase.addСard(card_series, card_number, card_status,
                                    current_discount, end_card, author)
                if not res:
                    flash("Ошибка создания карты", category='error')
                    count = int(count) + 1
                else:
                    flash('Карта добавлена успешно', category="success")
                continue
        else:
            card_series = request.form.get('card_series').upper()
            count = request.form.get('count')
            card_status = request.form.get('language')
            current_discount = request.form.get('current_discount')
            end_card = request.form.get('end_card')
            author = current_user.getName()

            while int(count) != 0:
                count = int(count) - 1
                card_number = random.randint(10000000, 99999999)
                res = dbase.addСard(card_series, card_number, card_status,
                                    current_discount, end_card, author)
                if not res:
                    flash("Ошибка создания карты", category='error')
                    count = int(count) + 1
                else:
                    flash('Карта добавлена успешно', category="success")
                continue

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

        # if user and check_password_hash(user['psw'], form.psw.data):
        if user and user['psw'] == hash.hexdigest():
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", form=form)

"""http://127.0.0.1:5000/register?csrf_token=ImVjZDExOTgzOTE5NzQ5M2YzOWNlZjI4Mjg3MGVmY2NiNzA0MTZhNzIi.YnDP1Q.2zuvpB4hCJYiHd3jCocbxOa-vKk&name=newuser3&email=new%40mail.com&psw=12345&psw2=12345&submit=%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F"""
@app.route("/register", methods=["POST", "GET"])
def register():
    csrf_token = request.args.get('csrf_token')
    name = request.args.get('name')
    email = request.args.get('email')
    psw = request.args.get('psw')
    psw2 = request.args.get('psw2')
    submit = request.args.get('submit')
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
            # hash = generate_password_hash(form.psw.data)
            res = dbase.addUser(form.name.data, form.email.data,
                                hash.hexdigest())
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
                return redirect(url_for('register'))

    return render_template("register.html", form=form)


@login_required
@app.route("/basket", methods=["POST", "GET"])
def basket():
    products = dbase.getProduct()
    print(products)
    author = current_user.getName()
    card = dbase.getCardsByName(author)
    if not products:
        flash("Ошибка получения продуктов", category='error')
        redirect(url_for('addProduct'))
    else:
        flash('Продукты загружены', category="success")

        # if card or products == False:
        #     return redirect(url_for('addСard'))
    if request.method == "POST":
        prod = request.form.get("language")
        card_number = request.form.get('language2')
        count = request.form.get('count')
        count = int(count)
        current_discount = dbase.getCardDiscount(card_number)
        current_discount = current_discount['current_discount']

        name_prod = prod.split(' |')[0]
        price = dbase.getProductPrice(name_prod.strip())

        price = price['discounted_price']
        price = price * count
        discount = str(
            count * price - (count * price * current_discount / 100))
        return order(count, name_prod, price, current_discount, discount,
                     card_number)

    return render_template("basket.html", product=products, card=card)


@app.route('/order')
@login_required
def order(count, name_prod, price, current_discount, discount, card_number):
    if request.method == "POST":
        res = dbase.CreateOrder(count, name_prod, price, current_discount,
                                discount, card_number)
        if res:
            flash("Заказ успешно создан", "success")
            return redirect(url_for('ShowCard', alias=card_number))
        else:
            flash("Ошибка ", "error")
    return render_template('orders.html', count=count, name_prod=name_prod,
                           price=price,
                           current_discount=current_discount,
                           card_number=card_number)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    if request.method == "POST":
        number = request.form.get('card_number')
        series = request.form.get('card_series')
        status = request.form.get('language')
        dis = request.form.get('current_discount')
        end_card = request.form.get('end_card')
        if number is not None:
            search = dbase.searchCard(number, series, status, dis, end_card)
            print(search)

            if not search:
                flash("Ошибка поиска карты", category='error')
            else:
                flash('Карта найдена', category="success")
                return render_template('search.html', search=search)
    if db:
        try:
            card = []
            card_unactive = []
            card_overdue = []
            author = current_user.getName()
            card = dbase.getCardsByName(author)
            if card:
                flash("Активные карты успешно загружены", "success")
                # return redirect(url_for('or'))
            else:
                flash("Активных карт не существует", "error")

            card_unactive = dbase.getCardsByName_unactive(author)
            if card_unactive:
                flash("Неактивные карты успешно загружены", "success")
                # return redirect(url_for('or'))
            else:
                flash("Неактивных карт не существует", "error")

            card_overdue = dbase.getCardsByName_overdue(author)
            if card_overdue:
                flash("Просроченные карты успешно загружены", "success")
                # return redirect(url_for('or'))
            else:
                flash("Просроченные карт не существует", "error")

            card_delete = dbase.getCardsByName_delete(author)

            if card_delete:
                flash("Карты из корзины успешно загружены", "success")
                # return redirect(url_for('or'))
            else:
                flash("Карты из корзины не найдены", "error")


        except Exception as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('profile.html', card=card,
                           card_unactive=card_unactive,
                           card_overdue=card_overdue, card_delete=card_delete)


@app.route("/card/<series>/<alias>", methods=["POST", "GET"])
@login_required
def ShowCard(alias,series):
    res = dbase.getCard(alias,series)
    if not res["owner"]:
        abort(404)
    orders = dbase.getOrders(alias)
    if not res["card_number"]:
        abort(404)

    if request.method == "POST":
        start_date = request.form.get('start_card')
        end_date = request.form.get('end_card')
        orders = dbase.getOrdersDate(alias, start_date, end_date)
        return render_template('card.html', card_series=res["card_series"],
                               card_number=res["card_number"],
                               data_card_create=res["data_card_create"],
                               owner=res["owner"],
                               current_discount=res["current_discount"],
                               data_card_end=res["data_card_end"],
                               data_card_last_use=res["data_card_last_use"],
                               total_sum=res["total_sum"],
                               card_status=res["card_status"],
                               orders=orders
                               )

    return render_template('card.html', card_series=res["card_series"],
                           card_number=res["card_number"],
                           data_card_create=res["data_card_create"],
                           owner=res["owner"],
                           current_discount=res["current_discount"],
                           data_card_end=res["data_card_end"],
                           data_card_last_use=res["data_card_last_use"],
                           total_sum=res["total_sum"],
                           card_status=res["card_status"],
                           orders=orders
                           )


@app.route("/card/deactivete/<series>/<number>")
@login_required
def CardDeactivate(series, number):
    res = dbase.CardDeactivate(series, number)
    if not res["card_status"]:
        abort(404)
    return redirect(url_for('profile'))


@app.route("/card/activate/<series>/<number>")
@login_required
def CardАctivate(series, number):
    res = dbase.CardАctivate(series, number)
    if not res["card_status"]:
        abort(404)
    return redirect(url_for('profile'))


@app.route("/card/tobasket/<series>/<number>")
@login_required
def ToBasket(series, number):
    res = dbase.ToBasket(series, number)
    if not res["card_status"]:
        abort(404)
    return redirect(url_for('profile'))


@app.route("/card/deletecard/<series>/<number>")
@login_required
def DeleteCard(series, number):
    res = dbase.DeleteCard(series, number)
    if not res["card_status"]:
        abort(404)
    return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(debug=True)
