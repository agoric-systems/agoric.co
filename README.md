```
# Running the web app locally for development on macOS

1) Download virtualenv / virtualenvwrapper.sh and create 
a new virtualenv. 

Using homebrew, this can be done with the following commands:

> brew install virtualenvwrapper.sh


2) Next, we want to create a new virtualenv using Python 3.5+.

On macOS the following env variables are necessary. 
You can set them by adding them to your ~/.profile

export WORKON_HOME=~/.venvs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
export PATH=/usr/local/bin:$PATH
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
export PKG_CONFIG_PATH="/usr/local/opt/openssl/lib/pkgconfig"
export FLASK_APP=agoricco
export FLASK_DEBUG=1


3) Now the virtualenv can be created.

> mkvirtualenv agoricco


4) Your prompt should say (agoricco) now.

5) Clone the project's git repo somewhere.

> git clone git@github.com:agoric-systems/agoric.co.git

6) Next, change into the project's directory.

> cd agoricco

7) Install the python dependencies.

> pip install -r requirements.txt

8) Change directory again into the agoricco directory
 and start the flask app.

> flask run

9) If you need to activate the virtualenv  again in the future:

> workon agoricco
```
