from wtforms import Form, StringField, TextAreaField, PasswordField, \
     validators, FieldList, SelectField, SelectMultipleField
from flask_wtf.file import FileField, FileRequired
from passlib.hash import sha256_crypt
#from wtforms.ext.dateutil.fields import DateField
from wtforms.fields.html5 import DateField
import dateutil
from mySql.check_queries import get_prose_types, get_poem_types

# Форма регистрации
class SignupForm(Form):
    login = StringField('Login', [validators.length(min=6, max=60),
                                  validators.InputRequired(),
                                  validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                          'letters or numbers')]
                        )
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
    login = StringField('Login or Email', [validators.length(min=6, max=60),
                                           validators.InputRequired(),
                                           validators.Regexp(regex="^[.@a-zA-z0-9а-яА-яіїІЇ]+$",
                                                             message='You can only use '
                                                                     'letters or numbers'
                                                                     'and symbols @ and .')]
                        )
    password = PasswordField('Password', [validators.length(min=6, max=60),
                                          validators.InputRequired(),
                                          validators.Regexp(regex="^[a-zA-z0-9]+$",
                                                            message='You can only use '
                                                                    'english letters '
                                                                    'or numbers')]
                             )


# Форма для редактирования основных данных пользователя
class EditUserInfoForm(Form):
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
        if user_info["user_name"][0]:
            self.name.data = user_info["user_name"][0]
        if user_info["user_surname"][0]:
            self.surname.data = user_info["user_surname"][0]
        if user_info["user_patronymic"][0]:
            self.patronymic.data = user_info["user_patronymic"][0]
        if user_info["user_phone"][0]:
            self.phone.data = user_info["user_phone"][0]
        if user_info["user_birth"][0]:
            self.birth.data = user_info["user_birth"][0]

    def fields(self):
        yield self.name.label, "\'" + self.name.data + "\'" if self.name.data else "\'\'"
        yield self.surname.label, "\'" + self.surname.data + "\'" if self.surname.data else "\'\'"
        yield self.patronymic.label, "\'" + self.patronymic.data + "\'" if self.patronymic.data else "\'\'"
        yield self.phone.label, "\'" + self.phone.data + "\'" if self.phone.data else "\'\'"
        yield self.birth.label, "\'" + str(self.birth.data) + "\'" if self.birth.data else "\'\'"
        raise StopIteration


class EditCreatorInfoForm(EditUserInfoForm):
    country = StringField("country", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9]+$", message='You can only use '
                                                                                        'english letters '
                                                                                        'or numbers'),
                                      validators.Optional()])
    city = StringField("city", [validators.length(min=0, max=60),
                                validators.Regexp(regex="^[a-zA-z0-9]+$", message='You can only use '
                                                                                    'english letters '
                                                                                    'or numbers'),
                                validators.Optional()])

    def change_info(self, user_info):
        super(EditCreatorInfoForm, self).change_info(user_info)
        if user_info["country"][0]:
            self.country.data = user_info["country"][0]
        if user_info["city"][0]:
            self.city.data = user_info["city"][0]

    def fields(self):
        yield self.country.label, "\'" + self.country.data + "\'" if self.country.data else "\'\'"
        yield self.city.label, "\'" + self.city.data + "\'" if self.city.data else "\'\'"
        raise StopIteration


class EditPublisherInfoForm(EditUserInfoForm):
    country = StringField("country", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                       'english letters '
                                                                                       'or numbers'),
                                     validators.Optional()])
    city = StringField("city", [validators.length(min=0, max=60),
                                      validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                        'english letters '
                                                                                        'or numbers'),
                                      validators.Optional()])
    street = StringField("street", [validators.length(min=0, max=60),
                                    validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                      'english letters '
                                                                                      'or numbers'),
                                    validators.Optional()])
    publisher_house_name = StringField("publisher_house_name", [validators.length(min=0, max=60),
                                    validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ]+$", message='You can only use '
                                                                                      'english letters '
                                                                                      'or numbers'),
                                    validators.Optional()])

    def change_info(self, user_info):
        super(EditPublisherInfoForm, self).change_info(user_info)
        if user_info["country"][0]:
            self.country.data = user_info["country"][0]
        if user_info["city"][0]:
            self.city.data = user_info["city"][0]
        if user_info["street"][0]:
            self.street.data = user_info["street"][0]
        if user_info["publisher_house_name"][0]:
            self.publisher_house_name.data = user_info["publisher_house_name"][0]

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

    file = FileField(validators=[FileRequired()])
    poem_types = SelectMultipleField(choices=[(i, i) for i in get_poem_types()])


class AddProseForm(Form):
    name = StringField("Name of prose", [validators.length(min=0, max=60),
                                     validators.Regexp(regex="^[a-zA-z0-9а-яА-яіїІЇ ]+$", message='You can only use '
                                                                                                 ' letters '
                                                                                                 'or numbers')]
                       )

    file = FileField(validators=[FileRequired()])
    prose_types = SelectMultipleField(choices=[(i, i) for i in get_prose_types()])




