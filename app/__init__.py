from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.payment_routes import payment_bp
    from app.routes.webhook_routes import webhook_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(payment_bp)           # tanpa prefix, agar / dan /transaksi jalan
    app.register_blueprint(webhook_bp, url_prefix='/api/webhook')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app