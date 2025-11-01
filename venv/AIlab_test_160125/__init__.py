from flask import Flask
from flask_socketio import SocketIO
import os
from . import db,auth,main
from AIlab_test_160125.main import handle_message

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( SECRET_KEY='e0e827d8a5ca9faa4a5c4e014cdf46ad08866ff85c1f4b9c06037af84e5bd633', DATABASE=os.path.join(app.instance_path, 'AIlab.sqlite'),)

    if test_config is None: app.config.from_pyfile('config.py', silent=True) # load the instance config, if it exists, when not testing
    else: app.config.from_mapping(test_config) # load the test config if passed in

    # ensure the instance folder exists
    try: os.makedirs(app.instance_path)
    except OSError: pass
    
    db.init_app(app)

    app.register_blueprint(auth.bp)

    socketio = SocketIO(app)

    if __name__ == '__main__': socketio.run(app)

    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    @socketio.on('message')
    def handle_message(msg):
        return main.handle_message(msg=msg)

    return app

