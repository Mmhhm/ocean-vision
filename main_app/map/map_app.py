import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,
                    cors_allowed_origins="*",
                    logger=True,
                    engineio_logger=True,
                    async_mode='eventlet')

objects = {}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    logger.info("Client connected")
    emit('update_objects', {'objects': objects})


@socketio.on('disconnect')
def on_disconnect():
    logger.info("Client disconnected")


if __name__ == '__main__':
    logger.info("Starting Flask-SocketIO server...")
    socketio.run(app, debug=True, port=5000, use_reloader=False)