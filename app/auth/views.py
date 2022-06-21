from flask import flash, redirect, render_template, request, url_for 
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
                flash('You have been logged in!', 'success')
            return redirect(next)
        flash('invalid credentials', 'success')
    return render_template('auth/login.html', form=form)


@auth.route('/me')
@login_required
def hh():
    return "hello"


@auth.route('/logout')
@login_required
def logout():
   logout_user()
   flash('you have logged out', 'success')
   return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('you have registered', 'success')
        print(user.gen_token())
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.before_app_request
def before_any_request():
    if current_user.is_authenticated and  request.blueprint != 'auth' and request.endpoint != 'static' and not current_user.confirmed:
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm_token(token):
        db.session.commit()
        flash("you have now confirmed")
        return redirect(url_for('main.index'))
    else:
        flash('invalid token or has expired', 'success')

    return redirect(url_for('main.index'))


    

    

    