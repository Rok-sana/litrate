import json

from flask import Flask, request, render_template, flash, url_for, redirect, session, send_from_directory
import classes.forms
from misc.configs import SECRET_KEY, USER_TYPES
from db_queries.get_queries import *
import db_queries.delete_queries
from db_queries.composition_work import *
from db_queries.collection_work import *
from db_queries.publisher_work import *
from db_queries.messages_work import *
from db_queries.update_queries import update_user_info, update_composition_edit_date
from db_queries.signingup import signup_user
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug.datastructures import CombinedMultiDict
from db_queries.file_adding import *
app = Flask(__name__)


# Обновлении информации о пользователе, который сейчас в системе
def update_session_user_info():
    session["user"].update(find_user_by_email(email=session["user"]["user_mail"]))
    if session["user_type"] == USER_TYPES.CREATOR:
        session["user"].update(find_creator_info(session["user_id"]))
        session["user"]["rating"] = get_creator_rating(session["user_id"], session["user_id"])
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
            flash("Вы не авторизированы! Войдите в систему!")
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
            flash("Вы не писатель!")
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
        if not find_user_by_email(email):
            # Если пользователь в базе не найден, регистрируем его
            signup_user(email, password, type)
            return redirect(url_for("signin"))
        else:
            flash("Найден пользователь с такой же почтой!", "error")
            # Иначе возвращаемся на страницу регистрации
    return render_template("signup.html", form=form)


# Страница входа в систему
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = classes.forms.SigninForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password_try = str(form.password.data)
        # Поиск совпадение в БД по почте
        found_user = find_user_by_email(email)
        if not found_user:
            # Если совпадения не найдено, то вернуться на страницу входа
            flash("Пользователь с такой почтой не найден", "error")
            return render_template("signin.html", form=form)

        # Если пользователь с такой почтой найден, то проверяем на совпадение пароли
        if not sha256_crypt.verify(password_try, found_user["user_password"]):
            # Пароли не совпали - возвращаемся на страницу входа
            flash("Пароли не совпадают", "error")
            return render_template("signin.html", form=form)

        # Пользователь вошел в систему, перенаправленно на начальную страницу
        flash("Вы успешно вошли в систему", "success")
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
    return user_profile(session["user_id"])


# Страница пользователя по id
@app.route("/profile/<int:user_id>",  methods=['GET', 'POST'])
def user_profile(user_id):
    user = find_user_by_id(user_id)
    if not user:
        return render_template("user_error.html")

    if request.method == 'POST':
        message_text = request.form.getlist("message_text")[0]
        if message_text:
            add_message(session["user_id"], user_id, message_text)
            flash("Сообщение отправлено")
        return redirect(request.referrer)

    if user["user_type"] == USER_TYPES.CREATOR:
        compositions = normalize_compositions(get_creators_compositions(user["user_id"], session.get("user_id")))
        poems = get_creator_poem(user["user_id"], session.get("user_id"))
        proses = get_creator_prose(user["user_id"], session.get("user_id"))
        poem_types, prose_types = get_creator_all_types(user["user_id"], session.get("user_id"))
        all_types = poem_types.copy()
        all_types.update(prose_types)
        collections = get_creator_collections(session["user_id"], session["user_id"])
        return render_template("user_creator_profile.html", compositions=compositions,
                               poems=poems, proses=proses,
                               poem_types=poem_types, prose_types=prose_types, types=all_types,
                               user=user, collections=collections)
    elif user["user_type"] == USER_TYPES.PUBLISHER:
        sent_collections = get_collections_to_publisher_by_status(session["user_id"], "Sent", session["user_id"])
        sent_proses = get_proses_to_publisher_by_status(session["user_id"], "Sent", session["user_id"])
        accepted_collections = get_collections_to_publisher_by_status(session["user_id"], "Accepted",
                                                                      session["user_id"])
        accepted_proses = get_proses_to_publisher_by_status(session["user_id"], "Accepted", session["user_id"])

        return render_template("user_publisher_profile.html", user=user, send_collections=sent_collections,
                               accepted_collections=accepted_collections,
                               sent_proses=sent_proses,
                               accepted_proses=accepted_proses)
    else:
        return render_template("user_moderator_profile.html", user=user)


# Страница редактирования данных пользователя
@app.route("/profile/edit",  methods=['GET', 'POST'])
@is_logged_in
def edit_info():
    update_session_user_info()
    if request.method == 'POST':
        form = get_edit_form(CombinedMultiDict((request.files, request.form)))
        if form.validate():
            if form.avatar.data:
                print(form.avatar.data)
            if form.avatar.data:
                add_avatar(form.avatar.data, session["user_id"])
            update_user_info(session["user_id"], form, session["user_type"])
            update_session_user_info()
            form.change_info(session["user"])
            flash("Изменения подтверждены!")
            return render_template("edit_user_info.html", form=form)
        else:
            flash("Введите данные корректно!")
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
            if form.file.data and validated_file(form.file.data):
                add_poem_by_file(form.file.data, form.name.data,
                                 request.form.getlist("poem_types"), session["user_id"])
            elif request.form.getlist("text")[0] != "":
                add_poem_by_text(request.form.getlist("text")[0], form.name.data,
                                 request.form.getlist("poem_types"), session["user_id"], session["user_id"])
            else:
                flash("Прикрепите файл или введите текст произведения в соответствующее поле!")
                types_json = json.dumps({x: x for x in get_poem_types()})
                return render_template("poem_adding.html", form=form, poem_types=types_json)
            flash("Сочинение добавлено!")
            update_session_user_info()
            return redirect(url_for("profile"))
        else:
            flash("Введите имя!")
            # !!!!
            types_json = json.dumps({x: x for x in get_poem_types()})
            return render_template("poem_adding.html", form=form, poem_types=types_json)
    else:
        form = classes.forms.AddPoemForm()
        types_json = json.dumps({x: x for x in get_poem_types()})
        return render_template("poem_adding.html", form=form, poem_types=types_json)


# Страница добавления прозаических произведений
@app.route('/prose_adding', methods=['GET', 'POST'])
@is_logged_in
@is_creator
def prose_adding():
    if request.method == 'POST':
        form = classes.forms.AddProseForm(CombinedMultiDict((request.files, request.form)))
        if form.validate():
            if form.file.data and validated_file(form.file.data):
                add_prose_by_file(form.file.data, form.name.data,
                                  request.form.getlist("prose_types"), session["user_id"])
            elif request.form.getlist("text")[0] != "":
                add_prose_by_text(request.form.getlist("text")[0], form.name.data,
                                  request.form.getlist("prose_types"), session["user_id"], session["user_id"])
            else:
                flash("Прикрепите файл или введите текст произведения в соответствующее поле!")
                types_json = json.dumps({x: x for x in get_prose_types()})
                return render_template("prose_adding.html", form=form, prose_types=types_json)
            flash("Сочинение добавлено!")
            update_session_user_info()
            return redirect(url_for("profile"))
        else:
            flash("Введите имя!")
            # !!!!
            types_json = json.dumps({x: x for x in get_prose_types()})
            return render_template("prose_adding.html", form=form, prose_types=types_json)
    else:
        form = classes.forms.AddProseForm()
        types_json = json.dumps({x: x for x in get_prose_types()})
        return render_template("prose_adding.html", form=form, prose_types=types_json)


# Перейти на страничку с произведением
@app.route('/composition/<int:composition_id>', methods=['GET', 'POST'])
def composition_page(composition_id):
    composition = get_composition(composition_id, session.get("user_id"))
    if not composition:
        return render_template('/errors/404.html'), 404
    if request.method == "POST":
        if composition.creator_id == session["user_id"]:
            if composition_is_used(composition.id):
                flash("Невозможно изменить произведение! Оно задействовано в сборниках!")
            else:
                text_of_comp = request.form.getlist("text")[0]
                rewrite_file(composition_id, text_of_comp, session["user_id"])
                update_composition_edit_date(composition_id)
                flash("Изменения подтверждены!")
        else:
            flash("У вас нету прав для этого действия!")
    return render_template("composition.html",
                           composition=get_composition(composition_id, session.get("user_id")),
                           text=get_composition_text(composition_id, session.get("user_id")))


# Поставить произведению лайк
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

    return redirect(request.referrer)
    return redirect(url_for('composition_page',composition_id=composition_id))


# Поставить произведению дизлайк
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

    return redirect(request.referrer)
    return redirect(url_for('composition_page',composition_id=composition_id))


# Удаление произведения
@app.route('/composition/<int:composition_id>/delete')
@is_logged_in
def delete_composition(composition_id):
    composition = get_composition(composition_id, session.get("user_id"))
    if composition and composition.creator_id == session["user_id"]:
        if composition.modifier == "Private":
            db_queries.delete_queries.delete_composition(composition_id)
        else:
            flash("Невозможно удалить произведение. Оно имеет статус 'Публичный'")

    return redirect(request.referrer)


# Страница поиска произведений
@app.route('/search/compositions',  methods=['GET', 'POST'])
def composition_search():
    if request.method == 'POST':
        search_string = request.form.getlist("search_string")[0].strip()
        composition_type = request.form.getlist("composition_type")[0]
        sort_type = request.form.getlist("sort_type")[0]
        compositions = find_compositions(name=search_string,
                                         user_id=session.get("user_id"),
                                         sort=sort_type,
                                         comp_type=composition_type)
    else:
        compositions = get_all_compositions(session.get("user_id"))
    return render_template("composition_search.html", compositions=compositions)


#
@app.route('/composition/<int:composition_id>/change_modifier',  methods=['GET', 'POST'])
def change_modifier(composition_id):
    composition = get_composition(composition_id, session.get("user_id"))
    if composition:
        if composition.creator_id == session.get("user_id"):
            if change_composition_modifier(composition_id):
                flash("Статус произведения успещно изменен!")
            else:
                flash("Невозможно изменить статус произведения! Оно задействовано в сборниках!")
        else:
            flash("У вас нету прав для этого действия!")

    return redirect(request.referrer)


# Страница поиска пользователей
@app.route('/search/user',  methods=['GET', 'POST'])
def user_search():
    if request.method == 'POST':
        search_string = request.form.getlist("search_string")[0].split()
        name = surname = ""
        if len(search_string) > 0:
            name = search_string[0]
        if len(search_string) > 1:
            surname = search_string[1]
        user_search_type = request.form.getlist("user_search_type")[0]
        sort_type = request.form.getlist("sort_type")[0]
        users = find_users_by_param_set(user_name=name,
                                        user_surname=surname,
                                        sort=sort_type,
                                        user_type=user_search_type)
    else:
        users = find_users_by_param_set(user_name="",
                                        user_surname="")
    return render_template("user_search.html", users=users)


# Страница создания сборника
@app.route('/collection_adding', methods=['GET', 'POST'])
@is_logged_in
@is_creator
def collection_adding():
    if request.method == 'POST':
        poems_to_add = list(map(int, request.form.getlist("choosed_poems")))
        if len(poems_to_add) < 15:
            flash("Выбрано слишком мало стихов! Нужно не меньше 15!")
            return redirect(request.referrer)
        else:
            if not request.form.getlist("collection_name"):
                flash("Некорректное имя!")
                return redirect(request.referrer)
            valid_poems = True
            for poem_id in poems_to_add:
                poem = get_composition(poem_id, session["user_id"])
                if not poem or poem.modifier == "Private":
                    valid_poems = False
                    break
            if valid_poems:
                add_collection(request.form.getlist("collection_name")[0],
                               session["user_id"], poems_to_add)
                flash("Сборник был успешно добавлен!")
            else:
                flash("Какой-то из стихов удален или имеет статус Приватный!")
                return redirect(request.referrer)
            return redirect(url_for("profile"))
    else:
        poems = dict()
        for poem in get_creator_poem(session["user_id"], session["user_id"]):
            if poem.modifier == "Public":
                poems[str(poem.id)] = poem.name
        return render_template("collection_adding.html", poems=json.dumps(poems))


# Перейти на страничку с
@app.route('/collection/<int:collection_id>', methods=['GET', 'POST'])
def collection_page(collection_id):
    coll, poems = get_collection(collection_id, session.get("user_id"))
    if not coll:
        return render_template('/errors/404.html'), 404
    if request.method == "POST":
        if coll.creator_id == session["user_id"]:
            pass
    return render_template("collection.html",
                           collection=coll,
                           poems=poems)


# Перейти на страничку с
@app.route('/collection/<int:collection_id>/delete', methods=['GET', 'POST'])
def collection_deleting(collection_id):
    coll = get_collection_by_id(collection_id)
    if coll["creator_id"] == session["user_id"]:
        if not collection_is_used:
            flash("Невозможно удалить сборник! ")
            return redirect(request.referrer)
        delete_collection_by_id(collection_id, session["user_id"])
        flash("Сборник успешно удален!")
        return redirect(url_for("profile"))
    else:
        flash("У вас нет прав для удаления сборника!")
        return redirect(request.referrer)


# Перейти на страничку с
@app.route('/collection_search', methods=['GET', 'POST'])
def collection_search():
    return render_template("collection_search.html", collections=get_all_collections(session["user_id"]))


# Написать сообщение пользователю по id
@app.route('/write/user_id=<int:user_id>&message=<string:message>')
@is_logged_in
def write_message(user_id, message):
    user = find_user_by_id(user_id)
    if user:
        add_message(session["user_id"], user_id, message)
    else:
        flash("Пользователь не найден!")
    return redirect(request.referrer)


@app.route("/messenger", methods=['GET', 'POST'])
@is_logged_in
def default_messenger():
    dialogs = get_dialogs_for_user(session["user_id"])
    if dialogs:
        key = list(dialogs.keys())[0]
        return messenger(key)
    return render_template("messenger.html", dialogs=dict())


@app.route("/messenger/<int:user_id>", methods=['GET', 'POST'])
@is_logged_in
def messenger(user_id):
    if request.method == 'POST':
        message = request.form.getlist("message_text")[0]
        to_user = request.form.getlist("to_user_id")[0]
        if message:
            add_message(session["user_id"], to_user, message)
    dialogs = get_dialogs_for_user(session["user_id"])
    if not dialogs.get(user_id):
        user_id = list(dialogs.keys())[0]
    return render_template("messenger.html", dialogs=dialogs,
                           to_user_id=user_id)


# Получить аватар пользователя
@app.route('/data/user_<int:user_id>/avatar')
def get_avatar(user_id):
    if os.path.exists('data/user_' + str(user_id) + "/avatar"):
        return send_from_directory('data/user_' + str(user_id), "avatar")
    return send_from_directory('static/images', "temp.jpg")


#
@app.route('/send_collection/publisher=<int:publisher_id>&collection=<int:collection_id>', methods=['GET', 'POST'])
def send_collection(publisher_id, collection_id):
    user = find_user_by_id(publisher_id)
    if not user:
        flash("no user with this id")
        return redirect(request.referrer)
    if user["user_type"] == USER_TYPES.PUBLISHER:
        if session["user_type"] == USER_TYPES.CREATOR:
            coll = get_collection(collection_id, session["user_id"])
            if coll[1]:
                print(coll)
                if coll[0]["creator_id"] == session["user_id"]:
                    if send_collection_to_publisher(collection_id, publisher_id):
                        flash("Success")
                    else:
                        flash("Collection was send earlier")
                else:
                    flash("You have no permission to sent this collection to publisher")
            else:
                flash("No collection with this id")
        else:
            flash("wrong operation")
    else:
        flash("wrong type")
    return redirect(request.referrer)


#
@app.route('/send_prose/publisher=<int:publisher_id>&prose=<int:prose_id>', methods=['GET', 'POST'])
def send_prose(publisher_id, prose_id):
    user = find_user_by_id(publisher_id)
    if not user:
        flash("no user with this id")
        return redirect(request.referrer)
    if user["user_type"] == USER_TYPES.PUBLISHER:
        if session["user_type"] == USER_TYPES.CREATOR:
            prose = get_composition(prose_id, session["user_id"])
            print(prose)
            if prose and prose.composition_type == "Prose":
                if prose.creator_id == session["user_id"]:
                    if send_prose_to_publisher(prose_id, publisher_id):
                        flash("Success")
                    else:
                        flash("Prose was send earlier")
                else:
                    flash("You have no permission to sent this prose to publisher")
            else:
                flash("No prose with this id found")
        else:
            flash("wrong operation")
    else:
        flash("wrong user type")
    return redirect(request.referrer)


@app.route('/send_collection_to_publisher/<int:publisher_id>', methods=['GET', 'POST'])
@is_logged_in
@is_creator
def send_collection_page(publisher_id):
    collections = get_creator_collections(session["user_id"], session["user_id"])
    print(collections)
    return render_template("send_collection_to_publisher.html", collections=collections, publisher_id=publisher_id)


@app.route('/send_prose_to_publisher/<int:publisher_id>', methods=['GET', 'POST'])
@is_logged_in
@is_creator
def send_prose_page(publisher_id):
    proses = get_creator_prose(session["user_id"], session["user_id"])
    return render_template("send_prose_to_publisher.html", proses=proses, publisher_id=publisher_id)


@app.route('/accept_prose/<int:prose_id>', methods=['GET', 'POST'])
@is_logged_in
def accept_prose(prose_id):
    if session["user"]["user_type"] == USER_TYPES.PUBLISHER:
        prose = find_prose_to_publisher(prose_id, session["user_id"])
        if prose["status"] == "Sent":
            modify_sent_prose_status(prose["offer_id"], "Accepted")
            flash("prose was accepted")
            prose = get_composition(prose_id, session["user_id"])
            message_text = "Ваш запрос на публикацию \"{0}\" был принят! " \
                           "Напишите для уточнения деталей!".format(prose.name)
            add_message(session["user_id"], prose.creator_id, message_text)
        else:
            flash("wrong prose status")
    else:
        flash("wrong user type")
    return redirect(request.referrer)


@app.route('/refuse_prose/<int:prose_id>', methods=['GET', 'POST'])
@is_logged_in
def refuse_prose(prose_id):
    if session["user"]["user_type"] == USER_TYPES.PUBLISHER:
        prose = find_prose_to_publisher(prose_id, session["user_id"])
        if prose["status"] == "Sent":
            modify_sent_prose_status(prose["offer_id"], "Refused")
            flash("prose was refused")
            prose = get_composition(prose_id, session["user_id"])
            message_text = "Ваш запрос на публикацию \"{0}\" был отклонен! " \
                           "Приносим свои извинения!".format(prose.name)
            add_message(session["user_id"], prose.creator_id, message_text)
        else:
            flash("wrong prose status")
        print(prose)
    else:
        flash("wrong user type")
    return redirect(request.referrer)


@app.route('/accept_collection/<int:collection_id>', methods=['GET', 'POST'])
@is_logged_in
def accept_collection(collection_id):
    if session["user"]["user_type"] == USER_TYPES.PUBLISHER:
        coll = find_collection_to_publisher(collection_id, session["user_id"])
        if coll["status"] == "Sent":
            modify_sent_collection_status(coll["offer_id"], "Accepted")
            flash("prose was accepted")
            message_text = "Ваш запрос на публикацию коллекции \"{0}\" был принят! " \
                           "Напишите для уточнения деталей!".format(coll["collection_name"])
            add_message(session["user_id"], coll["creator_id"], message_text)
        else:
            flash("wrong prose status")
        print(coll)
    else:
        flash("wrong user type")
    return redirect(request.referrer)


@app.route('/refuse_collection/<int:collection_id>', methods=['GET', 'POST'])
@is_logged_in
def refuse_collection(collection_id):
    if session["user"]["user_type"] == USER_TYPES.PUBLISHER:
        coll = find_collection_to_publisher(collection_id, session["user_id"])
        if coll["status"] == "Sent":
            modify_sent_collection_status(coll["offer_id"], "Refused")
            flash("prose was refused")
            message_text = "Ваш запрос на публикацию коллекции \"{0}\" был отклонен! " \
                           "Приносим свои извинения!".format(coll["collection_name"])
            add_message(session["user_id"], coll["creator_id"], message_text)
        else:
            flash("wrong prose status")
        print(coll)
    else:
        flash("wrong user type")
    return redirect(request.referrer)


@app.route('/sent_colletions', methods=['GET', 'POST'])
@is_logged_in
def sent_collections():
    sent_collections = get_collections_to_publisher_by_status(session["user_id"], "Sent", session["user_id"])
    return render_template("sent_collections.html",sent_collections=sent_collections)


@app.route('/sent_proses', methods=['GET', 'POST'])
@is_logged_in
def sent_proses():
    sent_proses = get_proses_to_publisher_by_status(session["user_id"], "Sent", session["user_id"])
    return render_template("sent_proses.html",sent_proses=sent_proses)


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
