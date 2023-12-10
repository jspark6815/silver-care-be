import os, threading
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_socketio import SocketIO
from api.auth import Auth
from api.notice import Notice
from api.task import Task

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': '*'}}) # Origin 전체 허용

api = Api(
    app,
    version='0.1',
    title="은빛 돌봄",
    terms_url="/",
    license="MIT",
    doc="/api-docs",
)

api.add_namespace(Auth, '/auth')
api.add_namespace(Notice, '/notice')
api.add_namespace(Task, '/task')

socketio = SocketIO(app)

if __name__ == "__main__":
    
    # app.run(host="0.0.0.0", debug=True, port=3000)

    socketio.run(app, host="0.0.0.0", debug=True, port=3000, allow_unsafe_werkzeug=True)
