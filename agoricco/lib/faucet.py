from agoricco import app 
from steem import Steem

s = None
creator = None

if 'FAUCET_ACTIVE_KEY' in app.config and 'FAUCET_ACCOUNT_NAME' in app.config:
    s = Steem(keys=[app.config['FAUCET_ACTIVE_KEY']])
    creator = app.config['FAUCET_ACCOUNT_NAME']


def register_account(account_name, owner_key, active_key, posting_key, memo_key):
    res = None
    password = None
    if s and creator:
        res = s.commit.create_account(account_name, owner_key=owner_key, 
            active_key=active_key, posting_key=posting_key, memo_key=memo_key,
            creator=creator)
        print(res)
    else:
        print('Faucet is not configured. Skipping account registration.')
    return (res, password)

def query_account(account_name):
    account = s.steemd.get_account(account_name)
    return account
