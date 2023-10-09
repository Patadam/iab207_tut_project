from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

app = Flask(__name__)

def create_app():
    
    app.secret_key="somethingsuperdupersecret"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)
    
    app.config['UPLOAD_FOLDER'] = '/static/image'
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    bootstrap = Bootstrap5(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html')

    return app