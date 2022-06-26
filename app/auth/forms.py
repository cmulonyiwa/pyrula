from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email,EqualTo
from wtforms.validators import ValidationError
from flask_login import current_user
from ..models import Role, User

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('login')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password1')])
    password1 = PasswordField('confirm password', validators=[DataRequired()])
    token = BooleanField('get token not using email')
    submit = SubmitField('register')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already registered.")

class UpdateUserProfileForm(FlaskForm):
    name = StringField('name')
    username = StringField('username')
    email = StringField('email', validators=[Email()])
    submit = SubmitField('update')

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class AdminProfileForm(FlaskForm):
    name = StringField('name')
    username = StringField('username')
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    email = StringField('email', validators=[Email()])
    submit = SubmitField('update')

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.role_name) for role in Role.query.order_by(Role.role_name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

