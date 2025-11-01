from flask import current_app, g
import sqlite3
import click

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect( current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None: db.close()

def init_db():
    db = get_db()
    db.executescript(
        """DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS coin_balance;

        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE coin_balance (
            user_id INTEGER PRIMARY KEY NOT NULL,
            gold INTEGER NOT NULL,
            silver INTEGER NOT NULL,
            copper INTEGER NOT NULL
        );"""
    )

@click.command('init-db')
def init_db_command():
#Clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
