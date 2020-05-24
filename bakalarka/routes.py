"""This is the routes module.

All routes(endpoints) provided for app.
"""

import os
import sys
import time 
import requests
import json
import flask
import httplib2 
import uuid 
from bakalarka import app, db, bcrypt, sched,jobs
from bakalarka.forms import  LoginForm
from bakalarka.models import User
from flask import render_template, url_for, flash, redirect, request,jsonify,Response
from flask_login import login_user, current_user, logout_user, login_required
from apiclient import discovery
from oauth2client import client
from googleapiclient import sample_tools
from rfc3339 import rfc3339
from dateutil import parser


@app.context_processor
def setWeather():
    """This is preprocesor function to set weather data.

    Requests weather data from api.openweathermap.org,time and date.
    
    Returns:
        A dict mapping keys to the corresponding data:
        {'weather': json,
         'time: time.strftime,
         'date: time.strftime,
         'wicon: string}
    """
    API_KEY = '1dc3d9ddda7b79c3e8e80ce27c139ae5'
    fcity = "Bratislava"
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    r = requests.get(url.format(fcity,API_KEY)).json() #API request to get weather data
    ftime = time.strftime('%H:%M:%S') #actual time(H:M:S)
    fdate = time.strftime('%A %B, %d-%m-%Y') #actual data(d-m-Y)
    icon = "http://openweathermap.org/img/w/{}.png".format(r["weather"][0]["icon"]) #url for weather icon
    
    return dict(weather=r,time = ftime,date=fdate,wicon=icon)


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
@login_required
def home():
    """This is the home route endpoint.

    If credentials are not set or authenticated, oauth2callback() is called.
    Credentials are stored in flask.session['credentials'].
    
    GET:
        responses:
            200:
                description: It renders the home.html template.
            302:
                description: Calls oauth2callback() to authenticate user.
    """
    if 'credentials' not in flask.session:
      return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    return render_template('home.html')


@app.route("/login",  methods=['GET', 'POST'])
def login():
    """This is the login route endpoint.

    Compare fetched data from LoginForm with database entries.

    POST:
        parameters:
            -   name: email
                in: path
                type: string
                required: true
                description: email to login
            -   name: password
                in: path
                type: string
                required: true
                description: password to login
        responses:
            302:
                description: User is uthenticated, redirect to /home
            200:
                description: User is not uthenticated, redirect to /login
    GET:
        responses:
            200:
                description: It renders the login.html template.  
                parameters:
                    -   
                        name: title
                        value: 'Login'
                        type: string
                        description: Title of page. 
                    -   name: form
                        value: form
                        type: LoginForm()
                        description: LoginForm object to fetch login data.   
    """   
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    """This is the logout route endpoint.

    Log out current user.
    
    GET:
        responses:
            302:
                description: Log out user and redirect to /home.           
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    """This is the account route endpoint.

    Prints APPSCEDULER jobs list into console.
    Redirect to /setCalendar to make list of possible callendar for user to sete.
    
    GET:
        responses:
            302:
                description: Redirect to /setCalendar.
    """
    print(sched.print_jobs())
    return flask.redirect(flask.url_for('setCalendar'))


@app.route("/scheduler")
@login_required
def scheduler():
    """This is the scheduler route endpoint.

    If calendarID is '-1'(default value), redirect to /setcalendar.
    Create iframe url for calendar.
    Load event data from events.json. 
    
    GET:
        responses:
            200:
                description: It renders the scheduler.html template.
                parameters:
                    -   name: src
                        value: src
                        type: string
                        description: Calendar URL to display in iframe.
                    -   name: events
                        value: data
                        type: json
                        description: Events data from Events.json
            302:
                description: CalendarID is not set, redirect to /setCalendar.  
    """
    cid = current_user.calendarID
    if(cid == '-1'):
        return flask.redirect(flask.url_for('setCalendar'))
    else:
        cname = current_user.calendarID   
        src = "https://calendar.google.com/calendar/embed?src="+cname 
        with open("bakalarka/static/events.json", 'r') as f:
            data = json.loads(f.read())                       
        return flask.render_template('scheduler.html',src=src,events=data)


@app.route("/setCalendar")
def setCalendar():
    """This is the setCalendar route endpoint.

    If credentials are not set or authenticated, oauth2callback() is called.
    Credentials are stored in flask.session['credentials'].
    Requests calendar list from GoogleCalendarAPI of logged user.
     

    GET:
        responses:
            200:
                description: It renders account.html.
                parameters:
                    -   name: calendars
                        value: calendars
                        type: list
                        description: List of current user Google Calendars.
            302:
                description: Calls oauth2callback() to authenticate user.     
    """    
    flask.session['next'] =  "setCalendar"
    if 'credentials' not in flask.session:
      return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())

    service = discovery.build('calendar', 'v3', http_auth)

    calendars = []    
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        calendars.append({"name": calendar_list_entry['summary'], "id": calendar_list_entry['id']})
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

    return  render_template(('account.html'),calendars=calendars)

  
@app.route('/updateCID',methods= ['POST'])
def updateCID():
    """This is the updateCID route endpoint.

    Endpoint to change value of current_user_calendarID column.
     
    POST:
        parameters:
            -   name: cid
                in: path
                type: string
                required: true
                description: New calendarID.  
        responses:
            204:
                description: calendarID column updated.
    """
    current_user.calendarID = request.form.get('cid')
    db.session.commit()
    return '', 204


@app.route('/oauth2callback')
def oauth2callback():
    """This is the oauth2callback route endpoint.

    
    This route/function is called by Google when user Accept/Refuse the consent of Google.
    Sets flask.session['credentials'].
     
    GET: 
        responses:
            302:
                description: Google login redirect.
            200:
                description: Redirect to /home.
    """ 
    flow = client.flow_from_clientsecrets(
    'client_secrets.json',['https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email'],
    redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('home'))


@app.route('/removeEntry', methods= ['POST'])
def removeEntry():
    """This is the removeEntry route endpoint.

    Endpoint to remove event from Google Calendar and Events.json.
    To remove Events.json entry deleteEvent() is called.

    POST:
        parameters:
            -   name: id
                in: path
                type: string
                required: true
                description: ID of event to remove. 
        responses:
            302:
                description: Event removed, redirect to /scheduler.
    """    
    flask.session['next'] =  "removeEntry"
    if 'credentials' not in flask.session:
      return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    mid = request.form.get('id')
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    imported_event = service.events().delete(calendarId=current_user.calendarID, eventId=mid).execute()

    deleteEvent(mid)
    return flask.redirect(url_for('scheduler'))


def deleteEvent(mid):   
    """Remove event from Events.json.

    Args:
        mid: ID of event to be removed.

    Returns:
        True for success, False otherwise.
    """
    with open("bakalarka/static/events.json", 'r') as f:
        data = json.loads(f.read()) 
        tmp = ""
        for den in data:
            for zaznam in data[den]:
                if zaznam['id'] == mid:
                    data[den].remove(zaznam)
                    if len(data[den]) == 0:
                        tmp = den
                        
                    
        if tmp != "":
            del data[tmp]
        with open("bakalarka/static/events.json", 'w') as f:
                f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    resetScheduler()
    return True


@app.route('/createEntry', methods= ['POST'])
def createEntry():
    """This is the createEntry route endpoint.

    Endpoint to create event in Google Calendar and Events.json.
    To add Events.json entry writeEvent() is called.

    POST:
        parameters:
            -   name: vyska
                in: path
                type: int
                required: true
                description: Height of blinds to be set. 
            -   name: uhol
                in: path
                type: int
                required: true
                description: Angle of blinds to be set. 
            -   name: date
                in: path
                type: date
                required: true
                description: Date of event to be executed.
            -   name: time
                in: path
                type: time
                required: true
                description: Time of event to be executed.
        responses:
            302:
                description: Event added, redirect to /scheduler.
    """ 
    flask.session['next'] =  "createEntry"
    if 'credentials' not in flask.session:
      return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    vyska = request.form.get('vyska')
    uhol = request.form.get('uhol')
    date = request.form.get('date')
    time = request.form.get('time')
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
    eventName = "@scheduled"
    eventID = str(uuid.uuid4())
    event = {
        'summary': eventName,
        'start': {
        'dateTime': date+"T"+time+":00",
        'timeZone': 'Europe/Prague',
        },
        'end': {
        'dateTime': date+"T"+time+":00",
        'timeZone': 'Europe/Prague',
        },
        'description': "Výška:"+vyska + " - Uhol:"+uhol,
        'icalUID ': eventID
    }
    imported_event = service.events().insert(calendarId=current_user.calendarID, body=event).execute()
    writeEvent(vyska,uhol,date,time,imported_event['id'])
    return flask.redirect(url_for('scheduler'))


def writeEvent(vyska,uhol,mdate,mtime,eventID):
    """Add event to Events.json.

    Args:
        vyska: Height of blinds to be set. 
        uhol: Height of blinds to be set.
        mdate: Height of blinds to be set.
        mtime: Height of blinds to be set.
        eventID: Google calendar eventID.

    Returns:
        True for success, False otherwise.
    """
    date = mdate
    event = [{}]
   
    with open("bakalarka/static/events.json", 'r') as f:
        data = json.loads(f.read()) 
        if date not in data:
            event = [{ "time":mtime,"vyska":vyska,"uhol":uhol,"id":eventID}]
            data[date] = event
        else:
            event = { "time":mtime,"vyska":vyska,"uhol":uhol, "id":eventID}
            data[date].append(event)

        with open("bakalarka/static/events.json", 'w') as f:
                f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    resetScheduler()
    return True


def resetScheduler():
    """Reset APPSCHEDULER job list for actual date

    Create acutal job list and set next restart to 00:00:00.

    Returns:
        True for success, False otherwise.
    """
    for job in sched.get_jobs():
        job.remove()
    jobs.initializer()
    sched.add_job(jobs.initializer,'cron',hour ='0')
    return True


@app.route('/work',methods=['POST'])
def work():
    """This is the work route endpoint.

    Endpoint to execute commands for I/O module.
    Currently in demo mode - print desired values into console. 

    POST:
        parameters:
            -   name: vyska
                in: path
                type: int
                required: true
                description: Height of blinds to be set. 
            -   name: uhol
                in: path
                type: int
                required: true
                description: Angle of blinds to be set. 
        responses:
            302:
                description: Print data and redirect to /home.
    """ 
    vyska = request.form.get('vyska')
    uhol = request.form.get('uhol')    
    print("Nastaví výšku: "+vyska+", uhol: "+uhol)     
    return flask.redirect(url_for('home'))    
       


