# backend/app.py

from flask import Flask
from backend.api.chat import chat_bp


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
