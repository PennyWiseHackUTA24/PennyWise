

from flask import Flask
from backend.api.chat import chat_bp, chat_api, chat_usrData


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(chat_api, url_prefix='/api')
    app.register_blueprint(chat_usrData, url_prefix='/api')
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)