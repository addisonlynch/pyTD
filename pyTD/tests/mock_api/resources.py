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

from functools import wraps
import json

from db.models.auth import Token
from db.engine import session
from db.models import (Account, CurrentBalances, InitialBalances,
                       ProjectedBalances, Client, Token)
from db.orm import AccountSchema, AuthTokenSchema

from flask import jsonify, request, render_template
from flask_restful import (Resource, abort, reqparse)


# def auth_check(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):

#     return decorated_function


class AccountResource(Resource):

    # @auth_check
    def get(self, account_id):

        access_token = request.headers.get("authorization")
        token_set = session.query(Token).\
                            filter_by(access_token=access_token).\
                            first()
        if not token_set:
            abort(403, message="Invalid auth token.")
        if not token_set.access_valid:
            return abort(403, message="Invalid auth token.")
        client_id = token_set.client_id
        client = session.query(Client).\
                         filter_by(client_id=client_id).\
                         first()
        if client.account.accountId != int(account_id):
            return abort(401, message="Not authorized.")
        accounts = session.query(Account).\
                           filter(Account.accountId == account_id).\
                           first()


        if not accounts:
            abort(404, message="Account %s doesn't exist." % account_id)
        schema = AccountSchema()
        return schema.dump(accounts)

    # @auth_check
    def post(self, account_id):
        json_data = request.get_json(force=True)

        # ensure account ID has been passed
        try:
            accountId = json_data["accountId"]
        except KeyError:
            abort(400, message="Invalid request. accountId must be provided.")

        # remove balances entries
        currentBalances = json_data.pop("currentBalances", None)
        initialBalances = json_data.pop("initialBalances", None)
        projectedBalances = json_data.pop("projectedBalances", None)

        # add account ID to balance objects
        if currentBalances:
            currentBalances["accountId"] = accountId
            c_model = CurrentBalances(**currentBalances)
            session.add(c_model)
        if initialBalances:
            initialBalances["accountId"] = accountId
            i_model = InitialBalances(**initialBalances)
            session.add(i_model)
        if projectedBalances:
            projectedBalances["accountId"] = accountId
            p_model = ProjectedBalances(**projectedBalances)
            session.add(p_model)

        account = Account(**json_data)

        session.add(account)
        session.commit()

        schema = AccountSchema()
        return schema.dumps(account)


class AuthResource(Resource):

    @staticmethod
    def verify_tokens(token, client_id):
        """
        Verify that a client is associated with a given access token

        Parameters
        ----------
        token: str
            Access token string
        client_id: str
            Client ID

        Errors
        ------
        """
        # Get the client associated with the token
        token = session.query(Token)\
                              .filter_by(client_id=client_id).first()

        # Abort if no client associated with this token
        if not token:
            abort(401, message="Auth token not valid.")

        # Returns the full token record
        return token


    def post(self, *args, **kwargs):
        """
        Post refresh token to receive access token
        """
        grant_type = request.form['grant_type']
        refresh_token = request.form['refresh_token']
        access_type = request.form['access_type']
        client_id = request.form['client_id']
        old_token = self.verify_tokens(refresh_token, client_id)
        session.delete(old_token)
        default_token = Token.generate_tokens()
        default_token["client_id"] = client_id
        new_token = Token(**default_token)
        session.add(new_token)
        session.commit()
        schema = AuthTokenSchema()
        return schema.dump(new_token)

# class AuthResource(Resource):

#     def get(*args, **kwargs):
#         """
#         Renders page for user to confirm the grant
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('client_id', type=str, help="Client ID")
#         args = parser.parse_args()

#         client_id = args.get('client_id')
#         client = Client.query.filter_by(client_id=client_id).first()
#         return render_template('oauthorize.html', **kwargs)

#     def post(*args, **kwargs):
#         """
#         Returns if user grants access or not
#         """
#         confirm = request.form.get('confirm', 'no')
#         return confirm == 'yes'
