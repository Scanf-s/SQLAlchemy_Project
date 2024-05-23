import secrets
import traceback
import requests
from typing import Tuple
from urllib.parse import urlencode

from faker import Faker
from faker_airtravel import AirTravelProvider
from flask import Flask, render_template, url_for, redirect, abort, session, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from sqlalchemy import Engine, Inspector
from sqlalchemy import inspect

from config.DatabaseInfo import DatabaseInfo
from config.database_utils import create_engine_connection, create_database_connection
from config.myGoogleClientKey import CLIENT_KEY, SECRET_KEY
from ui.user_interface import main_user_interface
from util.database_utils import execute_sql_file


def initialize_engine(db_info: DatabaseInfo) -> Tuple[Engine, Inspector]:
    """
    Initializes the SQLAlchemy engine and inspector, and executes the DDL script.

    @param db_info: DatabaseInfo object containing the database connection information
    @return: Tuple containing the SQLAlchemy engine and inspector objects
    """

    # DDL Setting
    engine = create_engine_connection(db_info)
    execute_sql_file(engine, "models/airport-ddl.sql")

    # DB Connection Setting
    db_connection_engine = create_database_connection(db_info)
    inspector = inspect(db_connection_engine)
    return db_connection_engine, inspector


def initialize_lib() -> Faker:
    """
    Initializes and returns a Faker instance with the AirTravelProvider.

    @return: Faker instance with AirTravelProvider added
    """

    # Library Initialize
    fake = Faker()
    fake.add_provider(AirTravelProvider)
    return fake


def main() -> None:
    """
    Main function to initialize the database connection, Faker library, and run the main user interface.

    @return: None
    """
    try:
        db_info = DatabaseInfo()
        db_connection_engine, inspector = initialize_engine(db_info)
        fake = initialize_lib()
        # RUN MAIN CODE
        main_user_interface(db_connection_engine, fake, inspector, db_info)
    except Exception as e:
        print(traceback.format_exc())


def create_app():
    new_flask_instance = Flask(__name__)
    try:
        db_info = DatabaseInfo()
    except Exception as e:
        print(traceback.format_exc())

    new_flask_instance.config.from_mapping(
        SECRET_KEY='test',
        SQLALCHEMY_DATABASE_URI=f"{db_info.database}://{db_info.username}:{db_info.password}@{db_info.address}:{db_info.port}/{db_info.database_name}",
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

    login = LoginManager(new_flask_instance)
    login.login_view = 'index'

    db = SQLAlchemy()
    class UserModel(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), nullable=False)
        email = db.Column(db.String(64), unique=True, nullable=False)

    db.init_app(new_flask_instance)
    with new_flask_instance.app_context():
        db.create_all()

    @login.user_loader
    def load_user(id):
        return UserModel.query.get(int(id))

    @new_flask_instance.route('/')
    def index():
        return render_template('index.html')

    @new_flask_instance.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('index'))

    @new_flask_instance.route("/hello/<text>")
    def hello(text: str):
        return f"{escape(text)}"

    @new_flask_instance.route("/authorize/<provider>")
    def oauth2_authorize(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))

        provider_data = new_flask_instance.config['OAUTH2_PROVIDERS'].get(provider)
        if not provider_data:
            abort(404)

        # generate a random string for the state parameter
        session['oauth2_state'] = secrets.token_urlsafe(16)

        # create a query string with all the OAuth2 parameters
        query_string = urlencode({
            'client_id': provider_data['client_id'],
            'redirect_uri': url_for('oauth2_callback', provider=provider,
                                    _external=True),
            'response_type': 'code',
            'scope': ' '.join(provider_data['scopes']),
            'state': session['oauth2_state'],
        })

        # redirect the user to the OAuth2 provider (google) authorization URL
        return redirect(provider_data['authorize_url'] + '?' + query_string)

    @new_flask_instance.route('/callback/<provider>')
    def oauth2_callback(provider):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))

        provider_data = new_flask_instance.config['OAUTH2_PROVIDERS'].get(provider)
        if provider_data is None:
            abort(404)

        # if there was an authentication error, flash the error messages and exit
        if 'error' in request.args:
            for k, v in request.args.items():
                if k.startswith('error'):
                    flash(f'{k}: {v}')
            return redirect(url_for('index'))

        # make sure that the state parameter matches the one we created in the
        # authorization request
        if request.args['state'] != session.get('oauth2_state'):
            abort(401)

        # make sure that the authorization code is present
        if 'code' not in request.args:
            abort(401)

        # exchange the authorization code for an access token
        response = requests.post(provider_data['token_url'], data={
            'client_id': provider_data['client_id'],
            'client_secret': provider_data['client_secret'],
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': url_for('oauth2_callback', provider=provider,
                                    _external=True),
        }, headers={'Accept': 'application/json'})
        if response.status_code != 200:
            abort(401)
        oauth2_token = response.json().get('access_token')
        if not oauth2_token:
            abort(401)

        # use the access token to get the user's email address
        response = requests.get(provider_data['userinfo']['url'], headers={
            'Authorization': 'Bearer ' + oauth2_token,
            'Accept': 'application/json',
        })
        if response.status_code != 200:
            abort(401)
        email = provider_data['userinfo']['email'](response.json())

        # find or create the user in the database
        with new_flask_instance.app_context():
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                user = UserModel(email=email, username=email.split('@')[0])
                db.session.add(user)
                db.session.commit()
                user = UserModel.query.filter_by(email=email).first()

        # log the user in
        login_user(user)
        return redirect(url_for('index'))

    return new_flask_instance


if __name__ == "__main__":
    # main()
    app = create_app()
    app.run(debug=True)
