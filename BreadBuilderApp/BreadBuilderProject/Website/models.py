# Laras + Keiths code for creating classes for database information

from . import db
from flask_login import UserMixin, current_user
from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, RadioField, HiddenField, StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange, DataRequired, ValidationError


# Creating user class with database model

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    income = db.Column(db.Float)
    accountType = db.Column(db.Float)


# Creating transaction class with transaction model

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(150))
    amount = db.Column(db.Float)
    dateDue = db.Column(db.DateTime, default=datetime.utcnow)
    frequency = db.Column(db.String)


# Form to update user profile details

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    income = FloatField('Income')

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
