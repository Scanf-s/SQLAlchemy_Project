from flask import Blueprint, redirect, url_for, abort, session, request, flash, current_app
from urllib.parse import urlencode
from flask_login import current_user, login_user, logout_user
import secrets
import requests
from models.UserModel import UserModel
from config.flask_sqlalchemy_init import db

oauth_blp = Blueprint('OAUTHBLUEPRINT', __name__)


@oauth_blp.route("/authorize/<provider>")
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if not provider_data:
        abort(404)

    session['oauth2_state'] = secrets.token_urlsafe(16)

    query_string = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('OAUTHBLUEPRINT.oauth2_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    return redirect(provider_data['authorize_url'] + '?' + query_string)


@oauth_blp.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('HOMEPAGEBLUEPRINT.home'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    if 'code' not in request.args:
        abort(401)

    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('OAUTHBLUEPRINT.oauth2_callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    with current_app.app_context():
        user = UserModel.query.filter_by(email=email).first()
        if user is None:
            user = UserModel(
                email=email,
                username=email.split('@')[0]
            )
            db.session.add(user)
            db.session.commit()
            user = UserModel.query.filter_by(email=email).first()

    login_user(user)
    return redirect(url_for('HOMEPAGEBLUEPRINT.home'))


@oauth_blp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
