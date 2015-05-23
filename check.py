import os
import tweepy
import requests
from twilio.rest import TwilioRestClient
from pymongo import MongoClient
from secret import TwilioSID, TwilioTOKEN, consumer_key, consumer_secret, access_token, access_token_secret


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)


mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
client = MongoClient(mongoUrl)
db = client.freebird
subscriptions = db.doctors        
for subscriber in subscriptions.find():
    name = subscriber['name']
    handle = subscriber['handle']
    number = subscriber['number']
    patientData = api.user_timeline(handle)
    for status in patientData:
        if str(status.text).find("I can't take it") and subscriber['sentMsg'] != 1:
            client = TwilioRestClient(TwilioSID, TwilioTOKEN)
            doctorMessage = "Hello " + name +",\n Your patient: "+handle+" needs urgent attention due to an alarming message submitted on twitter \n-FreeBird"
            doctorPhone = "+1"+number
            message = client.messages.create(body=doctorMessage,
                    to=doctorPhone,
                    from_="+17326540788") 
            db.doctors.update(subscriber,{"$set":{'sentMsg': 1}})             
            list(db.test.find()) 



