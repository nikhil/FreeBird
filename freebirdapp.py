import os
import requests
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from pymongo import MongoClient
import tweepy
import string
import numpy
from secret import TwilioSID, TwilioTOKEN, consumer_key, consumer_secret, access_token, access_token_secret


app = Flask(__name__)
app.config.from_pyfile('freebirdapp.cfg')

nutrientid = [301, 205, 601, 208, 291, 303, 304, 309, 255, 204]
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
    emptyList0 = []
    emptyList1 = []
    emptyList2 = []
    emptyList3 = []
    emptyList4 = []
    emptyList5 = []
    emptyList6 = []
    emptyList7 = []
    emptyList8 = []
    emptyList9 = []

    nutrientList[0] = emptyList0
    nutrientList[1] = emptyList1
    nutrientList[2] = emptyList2
    nutrientList[3] = emptyList3
    nutrientList[4] = emptyList4
    nutrientList[5] = emptyList5
    nutrientList[6] = emptyList6
    nutrientList[7] = emptyList7
    nutrientList[8] = emptyList8
    nutrientList[9] = emptyList9

    for status in result:
        firstSplit = str(status.text).split("f:")
        FoodOnStatus = firstSplit[1].split(",")
        needToAppend = True
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
                if needToAppend:
                    for SomeNutrient in foodnutrients:
                        if SomeNutrient['value'] != "--":
                            nutrientList[iterator].append(float(SomeNutrient['value']))
                        else:
                            nutrientList[iterator].append(0)
                        iterator = iterator +1
                        needToAppend = False
                else:
                    for SomeNutrient in foodnutrients:
                        if SomeNutrient['value'] != "--":
                            nutrientList[iterator][0]= nutrientList[iterator][0] + float(SomeNutrient['value'])
                        iterator = iterator +1

        secondSplit = firstSplit[0].split("i:")
        interaction = secondSplit[1].lstrip()
        interactList.append(float(interaction))
        thirdSplit = secondSplit[0].split("s:")
        sleep = thirdSplit[1].lstrip()
        sleepList.append(float(sleep))  
        journal = thirdSplit[0]
        print nutrientList
        Alchemyparams = {'apikey': 'd8894db2dd60aed653e7bd91ea854ce91f46ec85', 'text': str(journal), 'outputMode': 'json'}
        analyzedString = requests.get('http://access.alchemyapi.com/calls/text/TextGetTextSentiment',params=Alchemyparams).json()
        scoreList.append(float(analyzedString['docSentiment']['score']))
    maxc = 0
    maxstr = ""
    if abs(numpy.mean(numpy.corrcoef(scoreList,sleepList)[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,sleepList)[0])
        maxstr = "Sleep"
    if abs(numpy.mean(numpy.corrcoef(scoreList,interactList)[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,interactList)[0])
        maxstr = "Interactions"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[0])[0]))> abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[0])[0])
        maxstr = "Calcuim"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[1])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[1])[0])
        maxstr = "carbohydrate"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[2])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[2])[0])
        maxstr = "cholesterol"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[3])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[3])[0])
        maxstr = "energy"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[4])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[4])[0])
        maxstr = "Fiber"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[5])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[5])[0])
        maxstr = "Iron"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[6])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[6])[0])
        maxstr = "Magnesium"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[7])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[7])[0])
        maxstr = "zinc"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[8])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[8])[0])
        maxstr = "water"
    if abs(numpy.mean(numpy.corrcoef(scoreList,nutrientList[9])[0])) > abs(maxc):
        maxc = numpy.mean(numpy.corrcoef(scoreList,nutrientList[9])[0])
        maxstr = "fat"

    return render_template('PatientInfo.html',nutrientList=nutrientList,interactList=interactList,sleepList=sleepList,scoreList=scoreList,maxc=maxc,maxstr=maxstr,twitterHandle=twitterHandle) 
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


