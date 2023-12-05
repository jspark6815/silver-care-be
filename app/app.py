import os, threading
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from api.auth import Auth

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
