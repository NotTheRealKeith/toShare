# Laras + Keiths code for authorizing users and information

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)


# Labels, values and colours for pie chart


# Authorising form post from home page for transactions, sending to database

@auth.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        userid = current_user.id
        name = request.form.get('name')
        amount = request.form.get('amount')
        dateDue = request.form.get('dateDue')
        dateDue = datetime.strptime(dateDue, "%Y-%M-%d")
        frequency = request.form.get('frequency')

        if frequency == "1":
            frequency = "Once"
        elif frequency == "2":
            frequency = "Weekly"
        elif frequency == "3":
            frequency = "Fortnightly"
        elif frequency == "4":
            frequency = "Monthly"
        elif frequency == "5":
            frequency = "Yearly"

        new_trans = Transaction(userid=userid, name=name, amount=amount, dateDue=dateDue, frequency=frequency)
        db.session.add(new_trans)
        db.session.commit()
        flash(f'Transaction Created, {name}!', category='success')
        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)


# Showing a pie chart in reports page

@auth.route('/report')
def report():
    return render_template('report.html', title='Weekly Spending Graph', max=17000, set=zip(values, labels, colors))


# Authorising user login by checking their username and password with the database

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


# Logging out the user

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Signing up user through post form and sending the information to database

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.quiz'))

    return render_template("signup.html", user=current_user)


# Once user is signed up the template will show quiz page

@auth.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        accountType = request.form.get('accountType')

        if accountType == "1":
            accountType = 0.10
            flash("option 1 selected!!")

        elif accountType == "2":
            accountType = 0.30
            flash("Option 2 selected!!")

        elif accountType == "3":
            accountType = 0.50
            flash("Option 3 selected!!")

        elif accountType == "4":
            accountType = 0.80
            flash("Option 4 selected!!")

        newAccType = User(accountType=accountType)
        db.session.add(newAccType)
        db.session.commit()
        flash("Account Type has been selected!")
        return redirect(url_for('views.income'))

    return render_template('quiz.html', user=current_user)


# once the user has selected their account type they are asked for their weekly income

@auth.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        income = request.form.get('income')

        new_income = User(income=income)
        db.session.add(new_income)
        db.session.commit()
        flash(f'Income updated!', category='success')

    return render_template('home.html', user=current_user)
