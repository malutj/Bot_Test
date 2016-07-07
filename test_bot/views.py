from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
import requests
import appkey

# Create your views here.
def index ( request ):
    return HttpResponse("<h1>Home page</h1>")

def about ( request ):
    return HttpResponse("<h1>About Us</h1>")

def post_facebook_buttons ( fbid ):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + appkey.appkey
    response_msg = json.dumps ({"recipient":{"id":fbid},"message":{"attachment":{"type":"template","payload":{"template_type":"button","text":"Please make a selection","buttons":[{"type":"postback","title":"Make a fart noise","payload":"fart"},{"type":"postback","title":"Sing a song","payload":"song"},{"type":"postback","title":"Tell me a joke","payload":"joke"}]}}}})
    status = requests.post ( post_message_url, headers = {"Content-Type": "application/json"}, data=response_msg )


def post_facebook_message(fbid, received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + appkey.appkey
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":received_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def messageIsGreeting ( message ):
  if "Hello" in message['message']['text'] or "hello" in message['message']['text']:
      return True
  return False

def messageIsButtons ( message ):
  if "Button" in message['message']['text'] or "button" in message['message']['text']:
      return True
  return False

def handlePostback ( userid, payload ):
    if payload == 'fart':
        post_facebook_message ( userid, "pffffffttt")
    elif payload == 'song':
        post_facebook_message ( userid, "I like big butts and I cannot lie")
    elif payload == 'joke':
        post_facebook_message ( userid, "A guy walks into a bar. It hurt")


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
                print "MESSAGE RECEIVED:"
                print message
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    user_id = message['sender']['id']
                    # Print the message to the terminal
                    if ( messageIsGreeting ( message ) ):
                        response = requests.get ( 'https://graph.facebook.com/v2.6/' + user_id + '?access_token=' + appkey.appkey )
                        post_facebook_message ( user_id, "Hi there, " + response.json()['first_name'] )
                    elif ( messageIsButtons ( message ) ) :
                        post_facebook_buttons ( user_id )
                    else:
                        post_facebook_message ( user_id, message['message']['text'] )
                elif 'postback' in message:
                    user_id = message['sender']['id']
                    handlePostback ( user_id, message['postback']['payload'] )

        return HttpResponse()

    # Returns a Facebook user's firstname
    def GetUserFirstName ( userid ):
        response = requests.get ( 'https://graph.facebook.com/v2.6/' + userid + '?access_token=' + appkey.appkey )
        user_profile = response.json()

        if 'first_name' not in user_profile:
            return "buddy"
        else:
            return user_profile['first_name']