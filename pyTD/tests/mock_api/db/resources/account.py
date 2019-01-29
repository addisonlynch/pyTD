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

import json

from db.engine import session
from db.models import (Account, CurrentBalances, InitialBalances,
                       ProjectedBalances)
from db.orm import AccountSchema

from flask import jsonify, request
from flask_restful import (Resource, abort)


class AccountResource(Resource):

    def get(self, account_id):
        accounts = session.query(Account).\
                           filter(Account.accountId == account_id).\
                           first()

        if not accounts:
            abort(404, message="Account %s doesn't exist." % account_id)
        schema = AccountSchema()
        return schema.dump(accounts)

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
