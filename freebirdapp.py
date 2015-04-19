import os
import requests
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from pymongo import MongoClient
import tweepy
import string


app = Flask(__name__)
app.config.from_pyfile('freebirdapp.cfg')

consumer_key = 'srvKbL93bcw21SqEVg2err0f5'
consumer_secret = 'jx10iqIW2suFUNHbGcYZBcZStpVfuq4kiEKCpiQBvlybI4urV8'
access_token = '3167857703-tAu2B9E6rqRmzoqMvlzKMX4qdQUEcaoC4wnd4uP'
access_token_secret = 'rjOaYaXahSntjMgAazr1g7qpZzhP4drI4pFR0mbONqqn1'

nutrientid = [301, 205, 601, 208, 291, 303, 304, 406, 305, 306, 203, 307, 209, 269, 318,401,324,323,255,204]
nutrientid2 = [578, 401, 324, 323, 430, 255, 309, 204]


#caffeine 262
#calcium 301
#carbohydrate 205
#cholesterol 601
#energy 208 
#Fiber 291
#Iron 303
#Magnesium 304
#Niacin 406
#Phosphorus 305
#Potassium 306
#protein 203
#sodium 307
#starch 209
#sugar 269
#vitamin A 318
#vitamin B-12 578
#vitamin C 401
#vitamin D 324
#vitamin E 323
#vitamin K 430
#water 255
#zinc 309
#total fat 204
@app.route('/testTwitter')
def getTweets():
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/', methods=['POST'])
def my_form_post():

    twitterHandle = request.form['TwitterHandleBox']
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    result = api.user_timeline(twitterHandle)
    scoreList = []
    sleepList = []
    interactList = []
    foodList = []
    firstSplit= [0]*2
    secondSplit=[0]*2
    thirdSplit=[0]*2
    nutrientList = [0] *23
    emptyList = []
    for i in range(len(nutrientList)):
        nutrientList[i] = emptyList
    for status in result:
        firstSplit = str(status.text).split("f:")
        FoodOnStatus = firstSplit[1].split(",")
        for someFood in FoodOnStatus:
            foodtrimed1 = someFood.lstrip()
            foodtrimed2 = foodtrimed1.rstrip()
            nutritionParams = {'api_key': 'hUcSk43rUxao7dedHXut06RxFf4oo8mdtsagoFbv', 'q': foodtrimed2,'format': 'json', 'sort': 'r'}
            nutritionFood = requests.get('http://api.nal.usda.gov/usda/ndb/search',params = nutritionParams)
            if 'errors' not in nutritionFood.json():
                foodselected = nutritionFood.json()['list']['item'][0]['ndbno']
                nutrientsparams = {'api_key': 'hUcSk43rUxao7dedHXut06RxFf4oo8mdtsagoFbv','format':'json','ndbno': foodselected, 'nutrients':nutrientid}
                foodnutrients = requests.get('http://api.nal.usda.gov/usda/ndb/nutrients',params = nutrientsparams).json()
                foodnutrients = foodnutrients['report']['foods'][0]['nutrients']
                iterator = 0
                for SomeNutrient in foodnutrients:
                    if SomeNutrient['value'] != "--":
                        nutrientList[iterator].append(float(SomeNutrient['value']))
                    else:
                        nutrientList[iterator].append(0)
                    iterator = iterator +1
        secondSplit = firstSplit[0].split("i:")
        interaction = secondSplit[1].lstrip()
        interactList.append(interaction)
        thirdSplit = secondSplit[0].split("s:")
        sleep = thirdSplit[1].lstrip()
        sleepList.append(sleep)  
        journal = thirdSplit[0]
        Alchemyparams = {'apikey': 'd8894db2dd60aed653e7bd91ea854ce91f46ec85', 'text': str(journal), 'outputMode': 'json'}
        analyzedString = requests.get('http://access.alchemyapi.com/calls/text/TextGetTextSentiment',params=Alchemyparams).json()
        scoreList.append(analyzedString['docSentiment']['score'])
    return render_template('PatientInfo.html',nutrientList=nutrientList,interactList=interactList,sleepList=sleepList,scoreList=scoreList) 
@app.route('/subscribe',methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
        client = MongoClient(mongoUrl)
        db = client.freebird
        subscriptions = db.doctors        
        name = request.form['name']
        handle = request.form['handle']
        number = request.form['number']
        subscriber = {"name": name,
                "handle": handle,
                "number": number,
                "sentMsg": 0
                }
        subscriptions.insert(subscriber);
        return render_template('registered.html',name=name,handle=handle,number=number)
    else:
        return render_template('subscribe.html')
@app.route('/unsubscribe',methods=['GET','POST'])
def unsubscribe():
    if request.method == 'POST':
        mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
        client = MongoClient(mongoUrl)
        db = client.freebird
        subscriptions = db.doctors        
        name = request.form['name']
        handle = request.form['handle']
        number = request.form['number']
        subscriber = {"name": name,
                "handle": handle,
                "number": number}
        subscriptions.remove(subscriber);
        return render_template('unregistered.html',name=name,handle=handle,number=number)
    else:
        return render_template('unsubscribe.html')


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


