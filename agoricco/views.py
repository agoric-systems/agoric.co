from urllib3.exceptions import ReadTimeoutError
from agoricco import app
from .lib.account_codes import validate_code, burn_code
from .lib.faucet import register_account, query_account
from flask import render_template, request, flash, redirect, jsonify
from steembase.exceptions import RPCError, AccountExistsException
from sqlalchemy.exc import IntegrityError
from flask_babel import gettext, ngettext

@app.route('/', methods= ['GET'], subdomain='portal')
def portal_index():
    return redirect('/faucet')


@app.route('/about', methods=['GET'], subdomain='portal')
@app.route('/about', methods= ['GET'])
@app.route('/witness-proposal', methods=['GET'], subdomain='portal')
@app.route('/witness-proposal', methods= ['GET'])
@app.route('/faucet', methods=['GET'], subdomain='portal')
@app.route('/faucet', methods= ['GET'])
@app.route('/', methods= ['GET'])
def index():
    account_name = None
    password = None
    private_posting_key = None
    return render_template('index.html', account_name=account_name, password=password, private_posting_key=private_posting_key)


@app.route("/faucet", methods = ['POST'], subdomain='portal')
@app.route('/faucet', methods = ['POST'])
def faucet():
    success = None
    error = None
    info = None
    status = gettext(u'unknown')
    message = "unknown"
    try:
        password = None
        owner_key = None
        active_key = None
        private_posting_key = None
        if not request.form['account_name']:
            error = gettext(u'Please provide a desired account name.')
        elif request.form['code'] == "TESTCODE":
            password = "TEST PASS WORD"
            private_posting_key = "5TESTPRIVATEPOSTINGKEY"
            success = gettext(u'Test code used successfully.')
        elif request.form['code'] and validate_code(request.form['code']):
            if 'account_name' in request.form:
                (res, password) = register_account(
                    request.form['account_name'], 
                    request.form['owner_key'],
                    request.form['active_key'],
                    request.form['posting_key'],
                    request.form['memo_key'],
                )
                if res is not None and 'ref_block_num' in res:
                    # TODO: transfer prize amount to account (if any)
                    referrer = request.form['referrer_account'] if 'referrer_account' in request.form else None
                    burn_code(request.form['code'], request.form['account_name'], referrer=referrer)
                    success = gettext(u'Account created successfully!')
        else:
            error = gettext(u'The invite code could not be validated. Please check your code and try again.')
    except (AccountExistsException, IntegrityError) as e:
        error = gettext(u'The desired account name is already taken. Please choose another.')
    except RPCError as e:
        if ("Account name %s is invalid" % request.form['account_name']) in str(e):
            error = gettext(u'The desired account name is invalid. The name must have 3-16 alphanumeric characters and can not start with a number or include symbols other than periods, underscores, and hyphens.')
        if 'Insufficient balance to create account' in str(e):
            info = gettext(u'The account registration faucet has temporarily run out of funds. Please check back again later.')
    except ReadTimeoutError as e:
        info = gettext(u'There was an issue contacting the Steem network. Please try again.')
    if error is not None:
        status = 'error'
        message = error
    elif info is not None:
        status = 'info'
        message = info
    elif success is not None:
        status = 'success'
        message = success
    return jsonify(
        status=status, 
        message=message,
    )
