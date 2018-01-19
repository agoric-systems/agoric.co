from setuptools import setup

setup(
    name='agoricco',
    packages=['agoricco'],
    include_package_data=True,
    install_requires=[
        'flask==0.12.2',
        'flask_sqlalchemy==2.3.0',
        'flask_talisman==0.4.0',
        'steem==0.18.9',
        'funcy==1.8.0',
        'uwsgi',
        'flask-cors',
        'flask-seasurf',
        'mysqlclient',
        'Flask-Mobility',
    ],
)
