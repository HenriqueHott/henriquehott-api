from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importa e registra os blueprints (rotas)
    from app.routes.sentiments import sentiment_bp
    app.register_blueprint(sentiment_bp, url_prefix="/api")

    return app