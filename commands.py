import click
from app import db
from flask.cli import with_appcontext


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
    click.echo(f"Database Table Created")


@data.command()
@with_appcontext
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def dropdb():
    """Dropping all  database tables"""
    db.drop_all()
    click.echo('Dropped all tables!')