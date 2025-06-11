from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(message="Введите корректный email.")],
        render_kw={
            "id": "register-email",
            "class": "auth__input",
            "placeholder": "example@mail.com",
            "autocomplete": "email"
        }
    )
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={
            "id": "register-username",
            "class": "auth__input",
            "placeholder": "Например: fireman_91",
            "autocomplete": "username"
        }
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={
            "id": "register-password",
            "class": "auth__input",
            "placeholder": "Минимум 8 символов",
            "autocomplete": "new-password"
        }
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=8), EqualTo("password", message="Пароли должны совпадать")],
        render_kw={
            "id": "register-confirm-password",
            "class": "auth__input",
            "placeholder": "Ещё раз",
            "autocomplete": "new-password"
        }
    )
    submit = SubmitField("Регистрация", render_kw={"class": "auth__submit"})


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={
            "id": "login-username",
            "class": "auth__input",
            "placeholder": "example@mail.com или fireman_91",
            "autocomplete": "username"
        }
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={
            "id": "login-password",
            "class": "auth__input",
            "placeholder": "Введите пароль",
            "autocomplete": "current-password"
        }
    )
    submit = SubmitField("Войти", render_kw={"class": "auth__submit"})


class AddressForm(FlaskForm):
    city = StringField(
        "Город",
        validators=[DataRequired()],
        render_kw={
            "id": "address-city",
            "class": "modal__input",
            "placeholder": "Введите город",
            "autocomplete": "address-level2"
        }
    )
    street = StringField(
        "Улица",
        validators=[DataRequired()],
        render_kw={
            "id": "address-street",
            "class": "modal__input",
            "placeholder": "Введите улицу",
            "autocomplete": "address-line1"
        }
    )
    postcode = StringField(
        "Почтовый индекс",
        validators=[DataRequired()],
        render_kw={
            "id": "address-postcode",
            "class": "modal__input",
            "placeholder": "Введите почтовый индекс",
            "autocomplete": "postal-code"
        }
    )

    submit = SubmitField(
        "Сохранить",
        render_kw={
            "class": "modal__button modal__button--primary",
            "form": "addressForm",
            "data-action": "save"
        }
    )


class PersonalForm(FlaskForm):
    username = StringField(
        "Имя",
        validators=[DataRequired()],
        render_kw={
            "id": "personal-username",
            "class": "modal__input",
            "placeholder": "Введите имя",
            "autocomplete": "name"
        }
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(message="Введите корректный email.")],
        render_kw={
            "id": "personal-email",
            "class": "modal__input",
            "placeholder": "Введите email",
            "autocomplete": "email"
        }
    )
    phone = StringField(
        "Телефон",
        validators=[DataRequired()],
        render_kw={
            "id": "personal-phone",
            "class": "modal__input",
            "placeholder": "Введите телефон",
            "autocomplete": "tel"
        }
    )

    submit = SubmitField(
        "Сохранить",
        render_kw={
            "class": "modal__button modal__button--primary",
            "form": "personalForm",
            "data-action": "save"
        }
    )
