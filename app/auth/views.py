from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from ..models import User
from .forms import LoginForm


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
            return redirect(next)
        flash('invalid credentials', 'info')
    return render_template('auth/login.html', form=form)


@auth.route('/me')
@login_required
def hh():
    return "hello"


@auth.route('/lpgout')
@login_required
def logout():
   logout_user()
   flash('you have logged out', 'info')
   return redirect(url_for('main.index'))