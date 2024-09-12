from datetime import datetime
import pandas as pd
from sqlalchemy import null, text
from shop import db, login_manager, engine
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os


class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"'{self.id}', '{self.username}'"

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password,x):
        #print(self,"|",password,"|",x)
        return check_password_hash(self.password_hash,x)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))



class tweets(db.Model):
    username = db.Column(db.CHAR(20), nullable=False, primary_key = True)
    date = db.Column(db.Date, nullable=False, primary_key = True)
    content = db.Column(db.String(350), nullable=False)
    views = db.Column(db.INTEGER ,nullable=False)
    likes = db.Column(db.INTEGER, nullable=False)
    retweets = db.Column(db.INTEGER, nullable=False)
    comment = db.Column(db.INTEGER, nullable=False)
    score = db.Column(db.INTEGER, nullable=False)
    location = db.Column(db.VARCHAR(45), server_default=text('none'))
    categories = db.Column(db.VARCHAR(30), nullable=False)

#Test Data
CSV = pd.read_csv("../DATA.csv")

#New Database
df = pd.read_sql_table(table_name = "tweets", con = engine)
print(df)
CSV = CSV.iloc[: , 1:]

Categories = ["General Conspiracies","COVID-19/Vaccines","JFK","9/11","White Genocide","False Flags","Qanon","Russia/Ukraine War","Antisemitism","Economics","Secret Space Program","Climate Change","Satanic Panic","MH370","LGBTQ+","Flat Earth"]