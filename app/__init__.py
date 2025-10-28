from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login_citizen"

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.auth.routes import auth_bp
    from app.citizen.routes import citizen_bp
    from app.admin.routes import admin_bp
    from app.superadmin.routes import superadmin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp, url_prefix="/citizen")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(superadmin_bp, url_prefix="/superadmin")
    
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

    os.makedirs(app.config.get("UPLOAD_FOLDER", "app/static/uploads"), exist_ok=True)

    # ✅ FIX STARTS HERE
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # ✅ FIX ENDS HERE
    from datetime import timedelta
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    return app

