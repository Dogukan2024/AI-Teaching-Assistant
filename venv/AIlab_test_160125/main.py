from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, send, emit
from AIlab_test_160125.auth import login_required, load_logged_in_user
from AIlab_test_160125.db import get_db
from AIlab_test_160125.aiAPI import ask_to_ai
from AIlab_test_160125.warnings import *
import json, click

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html', coin_balance=get_coin_balance()[0])

def get_coin_balance():
    db=get_db()
    try: return db.execute("SELECT gold, silver, copper FROM coin_balance WHERE user_id = ?", (g.user["id"],)).fetchone(),db
    except: return {"gold":-1, "silver":-1, "copper":-1},None

def handle_message(msg):
    load_logged_in_user()

    if g.user is None:
        emit('message', {'type': 'error', 'content': warning_not_logged_in()})
        return

    click.echo(f"Received message: {msg}")

    try:
        msgjson = json.loads(msg)
        if msgjson["type"] != "message":
            emit('message', {'type': 'error', 'content': 'Invalid message type'})
            return

        selected_coin = msgjson["selected_coin"]
        coin_balance, db = get_coin_balance()
        remaining_coins = coin_balance[{"gold": 0, "silver": 1, "copper": 2}[selected_coin]]

    except Exception as e:
        click.echo(e)
        emit('message', {'type': 'error', 'content': warning_bad_message()})
        return

    if remaining_coins <= 0:
        click.echo("Not enough coins")
        emit('message', {'type': 'error', 'content': warning_not_enough_coins()})
        return

    # Deduct coin
    db.execute(f"UPDATE coin_balance SET {selected_coin} = ? WHERE user_id = ?", (remaining_coins - 1, g.user["id"]))
    db.commit()
    click.echo(f"Using {selected_coin} tier coin for question")

    @copy_current_request_context
    def stream_response():
        try:
            for chunk in ask_to_ai(msgjson["content"], tier =selected_coin):
                emit('message', {'type': 'stream', 'content': chunk})
        except Exception as e:
            emit('message', {'type': 'error', 'content': str(e)})
        finally:
            emit('message', {'type': 'done'})




    stream_response()