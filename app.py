from flask import Flask, render_template, url_for, redirect, flash
from flask_login import LoginManager, logout_user
from flask_migrate import Migrate
from flask_restx import Api

from config.DatabaseInfo import DatabaseInfo
from config.flask_sqlalchemy_init import db
from config.myGoogleClientKey import CLIENT_KEY, SECRET_KEY
from controller.homepage_controller import homepage_blp, dummy_api
from controller.oauth_controller import oauth_blp
from models.UserModel import UserModel

app = Flask(__name__)
db_connection_info = DatabaseInfo()

app.config.from_mapping(
    SECRET_KEY='test',
    SQLALCHEMY_DATABASE_URI=(
        f"{db_connection_info.database}://"
        f"{db_connection_info.username}:"
        f"{db_connection_info.password}@"
        f"{db_connection_info.address}:"
        f"{db_connection_info.port}/"
        f"{db_connection_info.database_name}"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    OAUTH2_PROVIDERS={
        'google': {
            'client_id': CLIENT_KEY,
            'client_secret': SECRET_KEY,
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'token_url': 'https://accounts.google.com/o/oauth2/token',
            'userinfo': {
                'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
                'email': lambda json: json['email'],
            },
            'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
        }
    }
)

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'index'


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(oauth_blp)
app.register_blueprint(homepage_blp)

api = Api(app, title='SQLAlchemy API', version='1.0', description='SQLAlchemy API', doc='/docs')
api.add_namespace(dummy_api)


if __name__ == "__main__":
    app.run(debug=True)