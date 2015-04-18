import tweepy
import requests
from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "ACd458c1d2873d89890101ad9ac3de1d3e" 
AUTH_TOKEN = "dc3394a65d05b60691348f75056bf943" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create( 
	from_="+17326540788",   
)

text = 'Hello how are you?'
#params3 = {'apikey': 'd8894db2dd60aed653e7bd91ea854ce91f46ec85', 'text': text, 'outputMode': 'json'}
#analyzedString = requests.get('http://access.alchemyapi.com/calls/text/TextGetTextSentiment',params=params3).json()
#print analyzedString['docSentiment']['score']



