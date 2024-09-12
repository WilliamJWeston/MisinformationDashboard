from datetime import datetime
from flask_wtf import FlaskForm
from pyparsing import Regex
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField, SelectField, SelectMultipleField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from shop.models import user, load_user
from flask import request
import re
Categories = ["General Conspiracies","COVID-19/Vaccines","JFK","9/11","White Genocide","False Flags","Qanon","Russia/Ukraine War","Antisemitism","Economics","Secret Space Program","Climate Change","Satanic Panic","MH370","LGBTQ+","Flat Earth"]
titles = ['2007-02.png', '2009-01.png', '2009-07.png', '2009-08.png', '2009-09.png', '2009-10.png', '2009-11.png', '2010-02.png', '2010-03.png', '2010-04.png', '2010-05.png', '2010-06.png', '2010-07.png', '2010-08.png', '2010-09.png', '2010-10.png', '2010-11.png', '2010-12.png', '2011-01.png', '2011-02.png', '2011-03.png', '2011-04.png', '2011-05.png', '2011-06.png', '2011-07.png', '2011-08.png', '2011-09.png', '2011-10.png', '2011-11.png', '2011-12.png', '2012-01.png', '2012-02.png', '2012-03.png', '2012-04.png', '2012-05.png', '2012-06.png', '2012-07.png', '2012-08.png', '2012-09.png', '2012-10.png', '2012-11.png', '2012-12.png', '2013-01.png', '2013-02.png', '2013-03.png', '2013-04.png', '2013-05.png', '2013-06.png', '2013-07.png', '2013-08.png', '2013-09.png', '2013-10.png', '2013-11.png', '2013-12.png', '2014-01.png', '2014-02.png', '2014-03.png', '2014-04.png', '2014-05.png', '2014-06.png', '2014-07.png', '2014-08.png', '2014-09.png', '2014-10.png', '2014-11.png', '2014-12.png', '2015-01.png', '2015-02.png', '2015-03.png', '2015-04.png', '2015-05.png', '2015-06.png', '2015-07.png', '2015-08.png', '2015-09.png', '2015-10.png', '2015-11.png', '2015-12.png', '2016-01.png', '2016-02.png', '2016-03.png', '2016-04.png', '2016-05.png', '2016-06.png', '2016-07.png', '2016-08.png', '2016-09.png', '2016-10.png', '2016-11.png', '2016-12.png', '2017-01.png', '2017-02.png', '2017-03.png', '2017-04.png', '2017-05.png', '2017-06.png', '2017-07.png', '2017-08.png', '2017-09.png', '2017-10.png', '2017-11.png', '2017-12.png', '2018-01.png', '2018-02.png', '2018-03.png', '2018-04.png', '2018-05.png', '2018-06.png', '2018-07.png', '2018-08.png', '2018-09.png', '2018-10.png', '2018-11.png', '2018-12.png', '2019-01.png', '2019-02.png', '2019-03.png', '2019-04.png', '2019-05.png', '2019-06.png', '2019-07.png', '2019-08.png', '2019-09.png', '2019-10.png', '2019-11.png', '2019-12.png', '2020-01.png', '2020-02.png', '2020-03.png', '2020-04.png', '2020-05.png', '2020-06.png', '2020-07.png', '2020-08.png', '2020-09.png', '2020-10.png', '2020-11.png', '2020-12.png', '2021-01.png', '2021-02.png', '2021-03.png', '2021-04.png', '2021-05.png', '2021-06.png', '2021-07.png', '2021-08.png', '2021-09.png', '2021-10.png', '2021-11.png', '2021-12.png', '2022-01.png', '2022-02.png', '2022-03.png', '2022-04.png', '2022-05.png', '2022-06.png', '2022-07.png', '2022-08.png', '2022-09.png', '2022-10.png', '2022-11.png', '2022-12.png', '2023-01.png', '2023-02.png', '2023-03.png', '2023-04.png', '2023-05.png']

class RegistrationForm(FlaskForm):
    username_new = StringField('Username',validators=[DataRequired()])
    password_new = PasswordField('Password',validators=[DataRequired(),EqualTo("password_confirm")])
    password_confirm = PasswordField('Confirm',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = user.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class CompareForm(FlaskForm):
    Cat1 = SelectField('Category1',choices=Categories)
    Cat2 = SelectField('Category2',choices=Categories)
    StartDate = DateField('Start Date', format='%Y-%m-%d',validators=[DataRequired()])
    EndDate = DateField('End Date', format='%Y-%m-%d',validators=[DataRequired()])
    Compare = SubmitField('Compare')

class CloudForm(FlaskForm):
    CatAll = SelectField('title',choices= titles)
    cloudSubmit = SubmitField('cloudSubmit')

class HomeForm(FlaskForm):
    Cats = SelectField('title', choices = Categories)
    homeSubmit = SubmitField('Submit')

class deleteForm(FlaskForm):
    delete = SubmitField('delete')
    