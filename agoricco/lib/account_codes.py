import random
import string
import csv
from agoricco import db
from agoricco.models import AccountCode


_generator = random.SystemRandom()


def generate_codes(quantity, prize_amount, prize_unit='STEEM'):
    for x in range(1, quantity):
        code = ''.join(_generator.choices(string.ascii_uppercase + string.digits, k=16))
        account_code = AccountCode(
            code=code, prize_amount=prize_amount, prize_unit=prize_unit)
        db.session.add(account_code)
    db.session.commit()


def load_codes(code_file_path, prize_amount=0, prize_unit='STEEM'):
    with open(code_file_path) as csvfile:
        code_reader = csv.DictReader(csvfile)
        for row in code_reader:
            account_code = AccountCode(
                code=row['code'], prize_amount=prize_amount, prize_unit=prize_unit)
            db.session.add(account_code)
        db.session.commit()


def normalize_code(account_code):
    return account_code.upper().replace('-', '').replace(' ', '')


def validate_code(account_code):
    try:
        valid_code = AccountCode.query.filter_by(code=normalize_code(account_code), consumed=False).first()
        if valid_code is not None:
            return True
    except Exception as e:
        print("failed to validate code: %s" % account_code)
    return False


def burn_code(account_code, registered_account, referrer=None):
    valid_code = AccountCode.query.filter_by(code=normalize_code(account_code), consumed=False).first()
    valid_code.registered_account = registered_account
    valid_code.consumed = True
    valid_code.referrer_account = referrer if referrer is not None else None
    db.session.commit()
