from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
import requests

# Create your views here.
def index ( request ):
  return HttpResponse("<h1>Home page</h1>")

def about ( request ):
  return HttpResponse("<h1>About Us</h1>")

def post_facebook_message(fbid, recevied_message):
  post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAY8WTjoQGkBAKrPfp0saKmatpHv3ZCmZCazHTRfSsAsTF80d0ZCk0d99eTL98AwHXAnGmUSNJVTzFtw7idje3Os0IAIGGBIFspvgh2NTxhABZBE6RZCmRE3e8WyRK2ne5xrtjE067o6tsJr8axZAkYJaYdydUexSbs81KiM7tAQZDZD'
  response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
  status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
  pprint(status.json())

def messageIsGreeting ( message ):
  if "Hello" in message['message']['text'] or "hello" in message['message']['text']:
      return True
  return False

class facebook_bot_view ( generic.View ):

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return generic.View.dispatch(self, request, *args, **kwargs)

  def get ( self, request, *args, **kwargs ):
    if self.request.GET['hub.verify_token'] == 'malutj':
      return HttpResponse(self.request.GET['hub.challenge'])
    else:
      print "Error in authentication"
      return HttpResponse("Error in authentication")

  def post ( self, request, *args, **kwargs ):
    # Converts the text payload into a python dictionary
    incoming_message = json.loads(self.request.body.decode('utf-8'))
    # Facebook recommends going through every entry since they might send
    # multiple messages in a single call during high load
    for entry in incoming_message['entry']:
      for message in entry['messaging']:
        # Check to make sure the received call is a message call
        # This might be delivery, optin, postback for other events
        if 'message' in message:
          # Print the message to the terminal
          if ( messageIsGreeting ( message ) ):
            user_profile = requests.get ( "https://graph.facebook.com/v2.6/"+message['sender']['id']+"?access_token=EAAY8WTjoQGkBAKrPfp0saKmatpHv3ZCmZCazHTRfSsAsTF80d0ZCk0d99eTL98AwHXAnGmUSNJVTzFtw7idje3Os0IAIGGBIFspvgh2NTxhABZBE6RZCmRE3e8WyRK2ne5xrtjE067o6tsJr8axZAkYJaYdydUexSbs81KiM7tAQZDZD" )
            pprint(user_profile.json())
            post_facebook_message ( message['sender']['id'], "Hi there, " + user_profile.json()['first_name'] )
          else:
            post_facebook_message(message['sender']['id'], message['message']['text'])
    return HttpResponse()

