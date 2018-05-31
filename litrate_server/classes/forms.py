from wtforms import Form, StringField, TextAreaField, PasswordField, \
     validators, FieldList, SelectField, SelectMultipleField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from passlib.hash import sha256_crypt
#from wtforms.ext.dateutil.fields import DateField
from wtforms.fields.html5 import DateField
import dateutil
from db_queries.get_queries import get_prose_types, get_poem_types


IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())
DOCUMENTS = tuple('rtf odf ods gnumeric abw doc docx xls xlsx'.split())
TEXT = ('txt',)


# Форма регистрации
class SignupForm(Form):
    password = PasswordField('Password', [validators.length(min=6, max=60),
                                          validators.InputRequired(),
                                          validators.EqualTo('confirm', message='Passwords do not match'),
                                          validators.Regexp(regex="^[a-zA-z0-9]+$", message='You can only use '
                                                                                            'english letters '
                                                                                            'or numbers')]
                             )
    confirm = PasswordField('Confirm password')

    email = StringField('Email', [validators.length(min=6, max=60), validators.Email()])
    type = SelectField('User type',
                       choices=[('Publisher', 'Publisher'), ('Creator', 'Creator')]
                       )


# Форма входа в систему
class SigninForm(Form):
    email = StringField('Email', [validators.length(min=6, max=60), validators.Email()])
    password = PasswordField('Password', [validators.length(min=6, max=60),
                                          validators.InputRequired(),
                                          validators.Regexp(regex="^[a-zA-z0-9]+$",
                                                            message='You can only use '
                                                                    'english letters '
                                                                    'or numbers')]
                             )


# Форма для редактирования основных данных пользователя
class EditUserInfoForm(Form):
    avatar = FileField(validators=[FileAllowed(IMAGES)])

    name = StringField("user_name", [validators.length(min=0, max=60),
                                validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                  'english letters '
                                                                                  'or numbers'),
                                validators.Optional()]
                       )
    surname = StringField("user_surname", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                        'english letters '
                                                                                        'or numbers'),
                                      validators.Optional()]
                          )
    patronymic = StringField("user_patronymic", [validators.length(min=0, max=60),
                                            validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$",
                                                              message='You can only use '
                                                                      'english letters '
                                                                      'or numbers'),
                                            validators.Optional()]
                             )
    phone = StringField("user_phone", [validators.length(min=0, max=60),
                                  validators.Regexp(regex="^[+][0-9]+$",
                                                    message='You can only use '
                                                            'numbers'),
                                  validators.Optional()]
                        )
    birth = DateField("user_birth", [validators.Optional()], format='%Y-%m-%d',
                      )

    def change_info(self, user_info):
        if user_info["user_name"]:
            self.name.data = user_info["user_name"]
        if user_info["user_surname"]:
            self.surname.data = user_info["user_surname"]
        if user_info["user_patronymic"]:
            self.patronymic.data = user_info["user_patronymic"]
        if user_info["user_phone"]:
            self.phone.data = user_info["user_phone"]
        if user_info["user_birth"]:
            self.birth.data = user_info["user_birth"]

    def fields(self):
        yield self.name.label, "\'" + self.name.data + "\'" if self.name.data else "\'\'"
        yield self.surname.label, "\'" + self.surname.data + "\'" if self.surname.data else "\'\'"
        yield self.patronymic.label, "\'" + self.patronymic.data + "\'" if self.patronymic.data else "\'\'"
        yield self.phone.label, "\'" + self.phone.data + "\'" if self.phone.data else "\'\'"
        yield self.birth.label, "\'" + str(self.birth.data) + "\'" if self.birth.data else "\'\'"
        raise StopIteration


class EditCreatorInfoForm(EditUserInfoForm):
    country = StringField("country", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                        'english letters '
                                                                                        'or numbers'),
                                      validators.Optional()])
    city = StringField("city", [validators.length(min=0, max=60),
                                validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                    'english letters '
                                                                                    'or numbers'),
                                validators.Optional()])

    def change_info(self, user_info):
        super(EditCreatorInfoForm, self).change_info(user_info)
        if user_info["country"]:
            self.country.data = user_info["country"]
        if user_info["city"]:
            self.city.data = user_info["city"]

    def fields(self):
        yield self.country.label, "\'" + self.country.data + "\'" if self.country.data else "\'\'"
        yield self.city.label, "\'" + self.city.data + "\'" if self.city.data else "\'\'"
        raise StopIteration


class EditPublisherInfoForm(EditUserInfoForm):
    country = StringField("country", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                       'english letters '
                                                                                       'or numbers'),
                                     validators.Optional()])
    city = StringField("city", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                        'english letters '
                                                                                        'or numbers'),
                                      validators.Optional()])
    street = StringField("street", [validators.length(min=0, max=60),
                                    validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                      'english letters '
                                                                                      'or numbers'),
                                    validators.Optional()])
    publisher_house_name = StringField("publisher_house_name", [validators.length(min=0, max=60),
                                    validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                      'english letters '
                                                                                      'or numbers'),
                                    validators.Optional()])

    def change_info(self, user_info):
        super(EditPublisherInfoForm, self).change_info(user_info)
        if user_info.get("country"):
            self.country.data = user_info["country"]
        if user_info.get("city"):
            self.city.data = user_info["city"]
        if user_info.get("street"):
            self.street.data = user_info["street"]
        if user_info.get("publisher_house_name"):
            self.publisher_house_name.data = user_info["publisher_house_name"]

    def fields(self):
        yield self.country.label, "\'" + self.country.data + "\'" if self.country.data else "\'\'"
        yield self.city.label, "\'" + self.city.data + "\'" if self.city.data else "\'\'"
        yield self.street.label, "\'" + self.street.data + "\'" if self.street.data else "\'\'"
        yield self.publisher_house_name.label, "\'" + self.publisher_house_name.data + "\'" \
                                               if self.publisher_house_name.data else "\'\'"
        raise StopIteration


class AddPoemForm(Form):
    name = StringField("Name of poem", [validators.length(min=0, max=60),
                                     validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                                 ' letters '
                                                                                                 'or numbers')]
                       )

    file = FileField(validators=[FileAllowed(DOCUMENTS + TEXT)])
    poem_types = SelectMultipleField(choices=[(i, i) for i in get_poem_types()])


class AddProseForm(Form):
    name = StringField("Name of prose", [validators.length(min=0, max=60),
                                     validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                                 ' letters '
                                                                                                 'or numbers')]
                       )

    file = FileField(validators=[FileAllowed(DOCUMENTS + TEXT)])
    prose_types = SelectMultipleField(choices=[(i, i) for i in get_prose_types()])




