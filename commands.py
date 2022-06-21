import re
import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Role

def password_validate(password):
    if len(password) < 8:
        return False
    return True

def email_validate(data):
    try:
        re_object = re.compile(r'[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)')
        match_object = re_object.match(data.strip())
    except Exception as t:
        print(t)
        print('check your email is correct')
        return False

    return  match_object


@click.group()
@with_appcontext
def data():
    """manange database CRUD"""
    pass 


@data.command()
@with_appcontext
def createdb():
    """create database tables"""
    db.create_all()
    Role.insert_role()
    click.echo(f"Database Table Created")


@data.command()
@with_appcontext
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def dropdb():
    """Dropping all  database tables"""
    db.drop_all()
    click.echo('Dropped all tables!')


@click.group()
@with_appcontext
def user():
    """adding to the database"""
    pass 



@user.command()
@with_appcontext
@click.option('--username', prompt='Your username please')
@click.option('--email', prompt='Your email please')
@click.option("--password", prompt='your password', hide_input=True,confirmation_prompt=True)
def adduser(username, email, password):
    "add all credentials to the database"
    try:
        email_data = email_validate(email)
        user = User.query.filter_by(email=email_data).first()
        if user:
            click.secho(f'this {email_data.string} is already  taken', fg='green', bold=True)
        if email_data.string != '':
            click.secho(f'add {email_data.string} to database', fg='green', bold=True)
        else:
            click.echo(email_data.string)
            return
    except AttributeError:
        click.secho('check your email in good'.upper(), fg='red', bold=True)
        return 

    pass_data = password_validate(password)
    if pass_data:
        click.secho(f'add your password to database', fg='green', bold=True)

    else:
        click.secho('check your password is greater than 8'.upper(), fg='red', bold=True)
        return

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    click.secho('you have been added to the database'.upper(), fg='blue', bold=True)





