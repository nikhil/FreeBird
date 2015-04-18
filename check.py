import tweepy
import requests
from twilio.rest import TwilioRestClient 

consumer_key = 'srvKbL93bcw21SqEVg2err0f5'
consumer_secret = 'jx10iqIW2suFUNHbGcYZBcZStpVfuq4kiEKCpiQBvlybI4urV8'
access_token = '3167857703-tAu2B9E6rqRmzoqMvlzKMX4qdQUEcaoC4wnd4uP'
access_token_secret = 'rjOaYaXahSntjMgAazr1g7qpZzhP4drI4pFR0mbONqqn1'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# put your own credentials here 
ACCOUNT_SID = "ACd458c1d2873d89890101ad9ac3de1d3e" 
AUTH_TOKEN = "dc3394a65d05b60691348f75056bf943" 

mongoUrl = os.environ['OPENSHIFT_MONGODB_DB_URL']
client = MongoClient(mongoUrl)
db = client.freebird
subscriptions = db.doctors        
for subscriber in subscriptions:
    name = subscriber['name']
    handle = subscriber['handle']
    number = subscriber['number']
    patientData = api.user_timeline(handle)
    for status in patientData:
        if str(status.text).find("I can't take it"):
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            doctorMessage = "Hello " + name +",\n You patient: "+handle+" needs urgent attention due to an alarming message submitted on twitter"
            doctorPhone = "+"+number
            message = client.messages.create(body=doctorMessage,
                    to=doctorPhone,
                    from_="+17326540788") 





