from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os,time,secrets

db = SQLAlchemy()
HOST = "localhost"
PORT = "5432"
USER = "admin"
PASSWORD = "GoofyAdmin"
DB_NAME = "dussdb"

def create_app():
    #app = Flask(__name__, static_folder='static')
    app = Flask(__name__)
    
    try: 
        sql_db_uri = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
        print(sql_db_uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = sql_db_uri
        app.secret_key = secrets.token_urlsafe(24)
        
        db.init_app(app)

        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        from website.models import CustomerAccount

        create_database(app)

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return CustomerAccount.query.get(int(id))
    except Exception as e:
        print(f"Failed to initialize the database: {e}")
        # Prevent the pod from crashing so I can launch iteractive shell and playaround
        while True:
            time.sleep(10)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
    print('Created DB')
    return