from flask import render_template, url_for, request, redirect, flash, session
from shop import app
from shop.models import user, db, CSV,Categories, df
from shop.models import user as U
from shop.forms import LoginForm, RegistrationForm, CompareForm, CloudForm, HomeForm
from flask_login import login_user, logout_user, current_user
from shop.scripts import CategoryCount
import datetime,pandas,re,numpy as np
import os

Categories = ["General Conspiracies","COVID-19/Vaccines","JFK","9/11","White Genocide","False Flags","Qanon","Russia/Ukraine War","Antisemitism","Economics","Secret Space Program","Climate Change","Satanic Panic","MH370","LGBTQ+","Flat Earth"]
titles = ['2007-02.png', '2009-01.png', '2009-07.png', '2009-08.png', '2009-09.png', '2009-10.png', '2009-11.png', '2010-02.png', '2010-03.png', '2010-04.png', '2010-05.png', '2010-06.png', '2010-07.png', '2010-08.png', '2010-09.png', '2010-10.png', '2010-11.png', '2010-12.png', '2011-01.png', '2011-02.png', '2011-03.png', '2011-04.png', '2011-05.png', '2011-06.png', '2011-07.png', '2011-08.png', '2011-09.png', '2011-10.png', '2011-11.png', '2011-12.png', '2012-01.png', '2012-02.png', '2012-03.png', '2012-04.png', '2012-05.png', '2012-06.png', '2012-07.png', '2012-08.png', '2012-09.png', '2012-10.png', '2012-11.png', '2012-12.png', '2013-01.png', '2013-02.png', '2013-03.png', '2013-04.png', '2013-05.png', '2013-06.png', '2013-07.png', '2013-08.png', '2013-09.png', '2013-10.png', '2013-11.png', '2013-12.png', '2014-01.png', '2014-02.png', '2014-03.png', '2014-04.png', '2014-05.png', '2014-06.png', '2014-07.png', '2014-08.png', '2014-09.png', '2014-10.png', '2014-11.png', '2014-12.png', '2015-01.png', '2015-02.png', '2015-03.png', '2015-04.png', '2015-05.png', '2015-06.png', '2015-07.png', '2015-08.png', '2015-09.png', '2015-10.png', '2015-11.png', '2015-12.png', '2016-01.png', '2016-02.png', '2016-03.png', '2016-04.png', '2016-05.png', '2016-06.png', '2016-07.png', '2016-08.png', '2016-09.png', '2016-10.png', '2016-11.png', '2016-12.png', '2017-01.png', '2017-02.png', '2017-03.png', '2017-04.png', '2017-05.png', '2017-06.png', '2017-07.png', '2017-08.png', '2017-09.png', '2017-10.png', '2017-11.png', '2017-12.png', '2018-01.png', '2018-02.png', '2018-03.png', '2018-04.png', '2018-05.png', '2018-06.png', '2018-07.png', '2018-08.png', '2018-09.png', '2018-10.png', '2018-11.png', '2018-12.png', '2019-01.png', '2019-02.png', '2019-03.png', '2019-04.png', '2019-05.png', '2019-06.png', '2019-07.png', '2019-08.png', '2019-09.png', '2019-10.png', '2019-11.png', '2019-12.png', '2020-01.png', '2020-02.png', '2020-03.png', '2020-04.png', '2020-05.png', '2020-06.png', '2020-07.png', '2020-08.png', '2020-09.png', '2020-10.png', '2020-11.png', '2020-12.png', '2021-01.png', '2021-02.png', '2021-03.png', '2021-04.png', '2021-05.png', '2021-06.png', '2021-07.png', '2021-08.png', '2021-09.png', '2021-10.png', '2021-11.png', '2021-12.png', '2022-01.png', '2022-02.png', '2022-03.png', '2022-04.png', '2022-05.png', '2022-06.png', '2022-07.png', '2022-08.png', '2022-09.png', '2022-10.png', '2022-11.png', '2022-12.png', '2023-01.png', '2023-02.png', '2023-03.png', '2023-04.png', '2023-05.png']
NoneType = type(None)

@app.route("/")
def script():
    return redirect(url_for('home'))

@app.route("/home", methods=['GET','POST'])
def home():
    #DATA IS REFERENCE TO THE PANDAS ARRAY
    form = HomeForm()
    Data = df 
    Cat = Categories[0]

    if form.validate_on_submit():
        Cat = form.Cats.data
    
    Ind = Categories.index(Cat)+1
    CatData = Data[Data['categories'].str.contains(r'\b'+str(Ind)+r'\b',regex=True)]
    Dates = []
    CatScore = []

    end_date = datetime.datetime.now()
    start_date = datetime.datetime.now() - datetime.timedelta(30)
    DateRange = pandas.date_range(start_date,end_date,inclusive='both')
    for date in DateRange:
        #For each date in range
        datestring = date.strftime("%d/%m/%Y")
        CatDateData = CatData[CatData['date'] == datestring] 
        CatScore.append(CatDateData['score'].sum())
        Dates.append(datestring)
        
    return render_template('home.html',form=form,Cat=Cat,packed = zip(Dates,CatScore))

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()

    #If register form is valid on submit
    if form.validate_on_submit():

        #Check that username is not too big or small
        if len(form.username_new.data) > 4 and len(form.username_new.data) < 21:

            #Add user to DB
            user = U(username=form.username_new.data, password=form.password_new.data)
            db.session.add(user)
            db.session.commit()

            #Log the user in
            user.authenticated = True
            login_user(user)

            return redirect(url_for('registered'))

    return render_template('register.html',title='Register',form=form)


@app.route("/registered")
def registered():
    return render_template('registered.html', title='Registered!')


@app.route("/loginerror")
def loginerror():
    return render_template('loginerror.html', title='Login Error!')


@app.route("/compare",methods=['GET','POST'])
def compare():
    form = CompareForm()
    form.Cat1.query = Categories
    form.Cat2.query = Categories

    #Default to first Category
    Cat1 = Categories[0]
    Cat2 = Categories[0]
    Dates = []
    Cat1Score = []
    Cat2Score = []
    
    #If Form submit is Valid
    if form.validate_on_submit():
        #Select Data
        Data = df

        #Get Categories
        Cat1 = form.Cat1.data
        Cat2 = form.Cat2.data
        Ind1 = Categories.index(Cat1)+1
        Ind2 = Categories.index(Cat2)+1

        #Get Dates
        StartDateObject = form.StartDate.data
        EndDateObject = form.EndDate.data
        StartDate = StartDateObject.strftime("%d/%m/%Y")
        EndDate = EndDateObject.strftime("%d/%m/%Y")

        #Get Category Data
        Cat1Data = Data[Data['categories'].str.contains(r'\b'+str(Ind1)+r'\b',regex=True)]
        Cat2Data = Data[Data['categories'].str.contains(r'\b'+str(Ind2)+r'\b',regex=True)]
        DateRange = pandas.date_range(StartDateObject,EndDateObject,inclusive='both')

        for date in DateRange:
            #For each date in range
            datestring = date.strftime("%d/%m/%Y")
            Cat1DateData = Cat1Data[Cat1Data['date'] == datestring]
            Cat2DateData = Cat2Data[Cat2Data['date'] == datestring]
            Cat1Score.append(Cat1DateData['score'].sum())
            Cat2Score.append(Cat2DateData['score'].sum())
            Dates.append(datestring)

    return render_template('compare.html', title='Compare Misinformation Topics',form=form, cat1=Cat1 , cat2=Cat2 , packed=zip(Dates,Cat1Score,Cat2Score) )

@app.route("/wordcloud",methods=['GET','POST'])
def wordcloud():
    form = CloudForm()
    form.CatAll.query = titles
    chosen = Categories[0]

    if form.validate_on_submit():
        chosen = form.CatAll.data
        print(chosen)


    path = "./wordclouds"
    cloudArray =[]
    # Loop through all files in the directory
    for filename in os.listdir(path):
        # Check if the file extension is a supported image format
        if filename.lower().endswith(('.png')):
            # If the file is an image, add its filename to the list
            cloudArray.append(filename)
    #print(cloudArray)
    return render_template('wordcloud.html', title='wordcloud',cloudList=cloudArray,form=form, chosenTitle=chosen)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()

    username = request.form.get("username")
    password = request.form.get('password')

    #If Form submit is Valid
    if form.validate_on_submit():
        user = U.query.filter_by(username=form.username.data).first()        
        #Throws error if username doesnt exist
        if type(user) == NoneType:
            flash('Enter a valid username')
            return render_template('loginerror.html')


        #If username does exist
        else:

            #Check password is valid
            print(user,password)
            print(user.verify_password(user,password))
            if (user.verify_password(user,password)):
                user.authenticated = True
                login_user(user)

                flash('Log in Sucessful')
                return redirect(url_for('home'))

            #Password wrong and throw error
            else:
                flash('Enter a valid password')
                return render_template('loginerror.html')

    return render_template('login.html',title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))