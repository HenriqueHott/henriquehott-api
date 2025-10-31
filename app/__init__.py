from flask import Flask
from app.routes.sentiments import sentiment_bp
from app.routes.posts import posts_bp
from mongoengine import connect
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(sentiment_bp, url_prefix="/api")
    app.register_blueprint(posts_bp, url_prefix="/api")
    connect(
        host=os.getenv("MONGODB_URI"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_PASSWORD"),
        db=os.getenv("MONGO_DATABASE"),
        authentication_source="admin"
    )
        
    return app