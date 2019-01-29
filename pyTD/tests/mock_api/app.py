# MIT License

# Copyright (c) 2018 Addison Lynch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime, timedelta

from flask import Flask, request
from flask_restful import Api
from flask_oauthlib.provider import OAuth2Provider

from db.engine import session
from db.models.auth import Client, Grant, Token
from db.models.user import User
from ext import oauth

from db.resources.account import AccountResource


def create_app():
    app = Flask(__name__)
    return app


def register_extensions():
    oauth.init_app(app)
    api.init_app(app)


app = create_app()
api = Api()
api.add_resource(AccountResource, '/v1/account/<account_id>',
                 endpoint='account')
register_extensions()

from settings import BASE_URL



# OAUTH INFO


# GET Client
@oauth.clientgetter
def load_client(client_id):
    return Client.queryfilter_by(client_id=client_id).first()


# GET/SET Grant
@oauth.grantgetter
def load_grant(client_id, code):
    Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=get_current_user(),
            expires=expires
        )
    session.add(grant)
    session.commit()
    return grant


# GET/SET Token
@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user_id=request.user_id)

    # Make sure that every client has only one token connected to a user
    for t in toks:
        session.delete(t)

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    session.add(tok)
    session.commit()
    return tok

# Au


# Utility function to get the current user
def get_current_user():
    # Use the client_id of the current request to get its user
    client_id = request.args['client_id']
    user = User.query.filter_by(client_id=client_id)
    return user.user_id

# Auth handler resource


if __name__ == "__main__":
    app = create_app()
    register_extensions()
    app.run(debug=True)
