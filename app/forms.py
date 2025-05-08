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
