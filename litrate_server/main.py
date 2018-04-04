from flask import Flask, request, render_template, flash, url_for, redirect, session, send_from_directory
import usefull_classes.forms
from misc.configs import SECRET_KEY, USER_TYPES
from mySql.check_queries import *
from mySql.update_queries import update_user_info
from mySql.signingup import signup_user
from passlib.hash import sha256_crypt
from functools import wraps
app = Flask(__name__)


# Обновлении информации о пользователе, который сейчас в системе
def update_session_user_info():
    session["user_info"].update(find_user(login=session["user_info"]["user_login"][0]))
    if session["user_type"] == USER_TYPES.CREATOR:
        session["user_info"].update(find_creator(session["user_id"]))
    elif session["user_type"] == USER_TYPES.PUBLISHER:
        session["user_info"].update(find_publisher(session["user_id"]))
    else:
        pass


def get_edit_form(req_form=None):
    if session["user_type"] == USER_TYPES.CREATOR:
        if req_form:
            return usefull_classes.forms.EditCreatorInfoForm(req_form)
        return usefull_classes.forms.EditCreatorInfoForm()
    elif session["user_type"] == USER_TYPES.PUBLISHER:
        if req_form:
            return usefull_classes.forms.EditPublisherInfoForm(req_form)
        return usefull_classes.forms.EditPublisherInfoForm()
    else:
        pass


# Функция, которая будет использоваться как декоратор
# Если пользователь вошел в систему, то вернет страницу, на которую пользователь переходил
# В другом случае предложит авторизироваться
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "signedin" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please sign in")
            return redirect(url_for("signin"))
    return wrap


# Начальная страница сайта
@app.route("/")
def index():
    return render_template("index.html")


# Страница регистрации пользователя
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = usefull_classes.forms.SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))  # Шифруем пароль
        type = form.type.data
        if not find_user(email, login):
            # Если пользователь в базе не найден, регистрируем его
            signup_user(login, email, password, type)
            return redirect(url_for("index"))
        else:
            # Иначе возвращаемся на страницу регистрации
            if find_user(email=email):
                flash("Another user with same email found", "error")
            else:
                flash("Another user with same login found", "error")
    return render_template("signup.html", form=form)


# Страница входа в систему
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = usefull_classes.forms.SigninForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        password_try = str(form.password.data)
        # Поиск совпадение в БД по почте
        found_user = find_user(email=login)
        # Поиск совпадения по логину
        if not found_user:
            found_user = find_user(login=login)
        if not found_user:
            # Если совпадения не найдено, то вернуться на страницу входа
            flash("User with this login or email not found", "error")
            return render_template("signin.html", form=form)

        # Если пользователь с такой почтой или логином найден, то проверяем на совпадение пароли
        if not sha256_crypt.verify(password_try, found_user['user_password'][0]):
            # Пароли не совпали - возвращаемся на страницу входа
            flash("Password do not match", "error")
            return render_template("signin.html", form=form)

        # Пользователь вошел в систему, перенаправленно на начальную страницу
        flash("You successfully signed in", "success")
        session["signedin"] = True
        session["user_id"] = found_user["user_id"][0]
        session["user_type"] = found_user["user_type"][0]
        session["user_info"] = found_user
        return redirect(url_for("index"))
    return render_template("signin.html", form=form)


# Выход пользователя из системы
@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))


# Страница профиля (разная для каждого типа пользователя)
@app.route("/profile")
@is_logged_in
def profile():
    update_session_user_info()
    if session["user_type"] == "Creator":
        return render_template("creator_profile.html")
    elif session["user_type"] == "Publisher":
        return render_template("publisher_profile.html")
    else:
        return render_template("moderator_profile.html")


# Страница редактирования данных пользователя
@app.route("/profile/edit",  methods=['GET', 'POST'])
@is_logged_in
def edit_info():
    update_session_user_info()
    if request.method == 'POST':
        form = get_edit_form(request.form)
        if form.validate():
            update_user_info(session["user_id"], form, session["user_type"])
            update_session_user_info()
            form.change_info(session["user_info"])
            flash("Change confirmed successfully")
            return render_template("edit_user_info.html", form=form)
        else:
            flash("Enter data correctly")
            # !!!!
            return render_template("edit_user_info.html", form=form)
    else:
        form = get_edit_form()
        form.change_info(session["user_info"])
        return render_template("edit_user_info.html", form=form)


# Получить какой-нибудь статический файл (js, css, ico...)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Страница не найдена
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/errors/404.html'), 404


# Ошибка сервера
@app.errorhandler(500)
def page_not_found(e):
    return render_template('/errors/500.html'), 500


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.run()
