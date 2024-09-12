import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine

#Flask Application Config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'wn6dX7yZIPmUWSpe7hBzWdM9g7vgHS9u'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Group7Best!@localhost/twitterdb'
db = SQLAlchemy(app)
engine = create_engine('mysql://root:Group7Best!@localhost:3306/twitterdb',echo = False)

print(engine)


#Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
