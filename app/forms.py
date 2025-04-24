from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, TelField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, Length, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    email = EmailField("Email",
                       validators=[DataRequired(), Email(message="Введите корректный email.")],
                       render_kw={
                           "id": "register-email",
                           "class": "auth__input",
                           "placeholder": "example@mail.com",
                           "autocomplete": "email"})
    username = StringField("Username", validators=[DataRequired()], render_kw={
        "id": "register-username",
        "class": "auth__input",
        "placeholder": "Например: fireman_91",
        "autocomplete": "username"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)], render_kw={
        "id": "register-password",
        "class": "auth__input",
        "placeholder": "Минимум 8 символов",
        "autocomplete": "new-password"})
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(),
                                                 Length(min=8),
                                                 EqualTo("password", message="Пароли должны совпадать")],
                                     render_kw={
                                         "id": "register-confirm-password",
                                         "class": "auth__input",
                                         "placeholder": "Ещё раз",
                                         "autocomplete": "new-password"})
    submit = SubmitField("Регистрация", render_kw={"class": "auth__submit"})


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={
        "id": "login-username",
        "class": "auth__input",
        "placeholder": "example@mail.com или fireman_91",
        "autocomplete": "username"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)], render_kw={
        "id": "login-password",
        "class": "auth__input",
        "placeholder": "Введите пароль",
        "autocomplete": "current-password"})
    submit = SubmitField("Войти", render_kw={"class": "auth__submit"})


class UpdateProfileForm(FlaskForm):
    email = EmailField("Email",
                       validators=[Optional(), Email(message="Введите корректный email.")],
                       render_kw={
                           "id": "update-email",
                           "class": "modal__input",
                           "placeholder": "example@mail.com",
                           "autocomplete": "email"})
    username = StringField("Username", validators=[Optional()], render_kw={
        "id": "update-username",
        "class": "modal__input",
        "placeholder": "fireman_91",
        "autocomplete": "username"})
    phone = TelField("Phone",
                     validators=[Optional(),
                                 Regexp(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$", message="Неверный формат телефона")],
                     render_kw={
                         "id": "update-phone",
                         "class": "modal__input",
                         "placeholder": "+7 (707) 123-45-67",
                         "type": "tel"})
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=8)], render_kw={
        "id": "update-new-password",
        "class": "modal__input",
        "placeholder": "Придумайте новый пароль",
        "autocomplete": "new-password"})
    current_password = PasswordField("Current Password", validators=[DataRequired(), Length(min=8)], render_kw={
        "id": "update-current-password",
        "class": "modal__input",
        "placeholder": "Пароль для подтверждения",
        "autocomplete": "current-password"})
    city = StringField("City", validators=[Optional()], render_kw={
        "id": "update-city",
        "class": "modal__input",
        "placeholder": "Алматы"})
    street = StringField("Street", validators=[Optional()], render_kw={
        "id": "update-street",
        "class": "modal__input",
        "placeholder": "пр. Абая, д. 10"})
    postcode = StringField("Postcode", validators=[Optional()], render_kw={
        "id": "update-postcode",
        "class": "modal__input",
        "placeholder": "050000"})
    submit = SubmitField("Сохранить", render_kw={"class": "button--default"})



class ContactForm(FlaskForm):
    name = StringField("Ваше имя", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Сообщение", validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField("Отправить")
