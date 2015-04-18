import os
import requests
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from pymongo import MongoClient
import tweepy


app = Flask(__name__)
app.config.from_pyfile('freebirdapp.cfg')

consumer_key = 'srvKbL93bcw21SqEVg2err0f5'
consumer_secret = 'jx10iqIW2suFUNHbGcYZBcZStpVfuq4kiEKCpiQBvlybI4urV8'
access_token = '3167857703-tAu2B9E6rqRmzoqMvlzKMX4qdQUEcaoC4wnd4uP'
access_token_secret = 'rjOaYaXahSntjMgAazr1g7qpZzhP4drI4pFR0mbONqqn1'


@app.route('/testTwitter')
def getTweets():
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    

@app.route('/')
def index():
    return render_template("my-form.html")
    #butts = "Butts are awesome"
    #return render_template('index.html',butts=butts)
@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    params3 = {'apikey': 'd8894db2dd60aed653e7bd91ea854ce91f46ec85', 'text': text, 'outputMode': 'json'}
    analyzedString = requests.get('http://access.alchemyapi.com/calls/text/TextGetTextSentiment',params=params3).json()
    return analyzedString['docSentiment']['score']
@app.route('/subscribe',methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
        client = MongoClient(mongoUrl)
        db = client.flask
        subscriptions = db.subscriptions        
        name = request.form['name']
        handle = request.form['handle']
        number = request.form['number']
        subscriber = {"name": name,
                "handle": handle,
                "number": number}
        subscriptions.insert(subscriber);
        return render_template('registered.html',name=name,handle=handle,number=number)
    else:
        return render_template('subscribe.html')

@app.route('/checklist')
def printlist():
    mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
    client = MongoClient(mongoUrl)
    db = client.flask
    subscriptions = db.subscriptions
    name= ""
    handle = ""
    number = ""
    for subscriber in subscriptions.find():
        name += subscriber['name']
        handle += subscriber['handle']
        number += subscriber['number']
    return render_template('registered.html',name=name,handle=handle,number=number)
     


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run(app.config['IP'], app.config['PORT'])


