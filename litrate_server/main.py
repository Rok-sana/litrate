from flask import Flask, request, render_template, flash, url_for, redirect, session, send_from_directory
import classes.forms
from misc.configs import SECRET_KEY, USER_TYPES
from db_queries.get_queries import *
import db_queries.delete_queries
from db_queries.update_queries import update_user_info
from db_queries.signingup import signup_user
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug.datastructures import CombinedMultiDict
from db_queries.file_adding import *
app = Flask(__name__)


# Обновлении информации о пользователе, который сейчас в системе
def update_session_user_info():
    session["user"].update(find_user(email=session["user"]["user_mail"]))
    if session["user_type"] == USER_TYPES.CREATOR:
        session["user"].update(find_creator_info(session["user_id"]))
        session["user"]["rating"] = get_creator_rating(session["user_id"])
    elif session["user_type"] == USER_TYPES.PUBLISHER:
        session["user"].update(find_publisher_info(session["user_id"]))
    else:
        pass


def get_edit_form(req_form=None):
    if session["user_type"] == USER_TYPES.CREATOR:
        if req_form:
            return classes.forms.EditCreatorInfoForm(req_form)
        return classes.forms.EditCreatorInfoForm()
    elif session["user_type"] == USER_TYPES.PUBLISHER:
        if req_form:
            return classes.forms.EditPublisherInfoForm(req_form)
        return classes.forms.EditPublisherInfoForm()
    else:
        pass


#
def normalize_compositions(compositions, number_of_compositions=5):
    res = []
    for i in range(min(len(compositions), number_of_compositions)):
        res.append(compositions[i])
    return res


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


# Возвращает страницу, если пользователь является писателем,
# иначе переведет его на начальную страницу
def is_creator(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["user_type"] == USER_TYPES.CREATOR:
            return f(*args, **kwargs)
        else:
            flash("You are not creator!")
            return redirect(url_for("profile"))
    return wrap


# Начальная страница сайта
@app.route("/")
def index():
    return render_template("index.html")


# Страница регистрации пользователя
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = classes.forms.SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))  # Шифруем пароль
        type = form.type.data
        if not find_user(email):
            # Если пользователь в базе не найден, регистрируем его
            signup_user(email, password, type)
            return redirect(url_for("signin"))
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
    form = classes.forms.SigninForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password_try = str(form.password.data)
        # Поиск совпадение в БД по почте
        found_user = find_user(email)
        if not found_user:
            # Если совпадения не найдено, то вернуться на страницу входа
            flash("User with this email not found", "error")
            return render_template("signin.html", form=form)

        # Если пользователь с такой почтой найден, то проверяем на совпадение пароли
        if not sha256_crypt.verify(password_try, found_user["user_password"]):
            # Пароли не совпали - возвращаемся на страницу входа
            flash("Password do not match", "error")
            return render_template("signin.html", form=form)

        # Пользователь вошел в систему, перенаправленно на начальную страницу
        flash("You successfully signed in", "success")
        session["signedin"] = True
        session["user_id"] = found_user["user_id"]
        session["user_type"] = found_user["user_type"]
        session["user"] = found_user
        return redirect(url_for("profile"))
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
    if session["user_type"] == USER_TYPES.CREATOR:
        compositions = normalize_compositions(get_creators_compositions(session["user_id"]))
        return render_template("creator_profile.html", compositions=compositions)
    elif session["user_type"] == USER_TYPES.PUBLISHER:
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
            form.change_info(session["user"])
            flash("Change confirmed successfully")
            return render_template("edit_user_info.html", form=form)
        else:
            flash("Enter data correctly")
            # !!!!
            return render_template("edit_user_info.html", form=form)
    else:
        form = get_edit_form()
        form.change_info(session["user"])
        return render_template("edit_user_info.html", form=form)


# Страница добавления стихов
@app.route('/poem_adding', methods=['GET', 'POST'])
@is_logged_in
@is_creator
def poem_adding():
    if request.method == 'POST':
        form = classes.forms.AddPoemForm(CombinedMultiDict((request.files, request.form)))
        if form.validate():
            add_poem(form.file.data, form.name.data, form.poem_types.data, session["user_id"])
            flash("Poem added")
            update_session_user_info()
            return redirect(url_for("profile"))
        else:
            flash("Something go wrong")
            # !!!!
            return render_template("poem_adding.html", form=form)
    else:
        form = classes.forms.AddPoemForm()
        return render_template("poem_adding.html", form=form)


# Страница добавления прозаических произведений
@app.route('/prose_adding', methods=['GET', 'POST'])
@is_logged_in
@is_creator
def prose_adding():
    if request.method == 'POST':
        form = classes.forms.AddProseForm(CombinedMultiDict((request.files, request.form)))
        if form.validate():
            add_prose(form.file.data, form.name.data, form.prose_types.data, session["user_id"])
            flash("Prose added")
            update_session_user_info()
            return redirect(url_for("profile"))
        else:
            flash("Something go wrong")
            # !!!!
            return render_template("prose_adding.html", form=form)
    else:
        form = classes.forms.AddProseForm()
        return render_template("prose_adding.html", form=form)


# Перейти на страничку с произведением
@app.route('/composition/<int:composition_id>')
def composition_page(composition_id):
    return render_template("composition.html",
                           composition=get_composition(composition_id))


#
@app.route('/composition/<int:composition_id>/like')
@is_logged_in
def like_composition(composition_id):
    mark = get_like_to_composition_from_user(composition_id, session["user_id"])
    if not mark:
        insert_compositions_marks(composition_id, session["user_id"], 1)
    else:
        db_queries.delete_queries.delete_compositions_marks(composition_id, session["user_id"])
        if mark == -1:
            insert_compositions_marks(composition_id, session["user_id"], 1)

    return redirect(url_for('composition_page',composition_id=composition_id))


#
@app.route('/composition/<int:composition_id>/dislike')
@is_logged_in
def dislike_composition(composition_id):
    mark = get_like_to_composition_from_user(composition_id, session["user_id"])
    if not mark:
        insert_compositions_marks(composition_id, session["user_id"], -1)
    else:
        db_queries.delete_queries.delete_compositions_marks(composition_id, session["user_id"])
        if mark == 1:
            insert_compositions_marks(composition_id, session["user_id"], -1)
    return redirect(url_for('composition_page',composition_id=composition_id))


#
@app.route('/composition/<int:composition_id>/delete')
@is_logged_in
def delete_composition(composition_id):
    composition = get_composition(composition_id)
    if composition and composition.creator_id == session["user_id"]:
        if composition.modifier == "Private":
            db_queries.delete_queries.delete_composition(composition_id)
        else:
            flash("Невозможно удалить произведение. Оно имеет статус 'Публичный'")

    return redirect(url_for('profile'))


#
@app.route('/search/compositions')
def composition_search():
    compositions = get_all_compositions()
    return render_template("composition_search.html", compositions=compositions)


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
