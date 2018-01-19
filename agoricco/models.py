from agoricco import db

class AccountCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)
    consumed = db.Column(db.Boolean(), default=False)
    registered_account = db.Column(db.String(16), unique=True)
    referrer_account = db.Column(db.String(16))
    prize_amount = db.Column(db.Integer, nullable=False, default=0)
    prize_unit = db.Column(db.String(16), nullable=False, default="STEEM")
