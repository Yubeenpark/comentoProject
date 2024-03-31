'''from django.shortcuts import redirect
import json
from django.http import HttpResponse
from flask import Flask, redirect, url_for, request
from .forms import SignupForm, LoginForm

app = 'social'

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import InstalledAppFlow
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import Flow
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
flow =  google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secrets.json',
    scopes = ['openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ],
)

# Tell the user to go to the authorization URL.

flow.redirect_uri = 'http://ec2-3-34-90-91.ap-northeast-2.compute.amazonaws.com:8000/social/google/login/callback/'

authorization_url, state = flow.authorization_url(
    access_type='online',
    include_granted_scopes='true')
    
    
def verify_id_token(credentials):
    idinfo = id_token.verify_oauth2_token(credentials.id_token, 
        requests.Request(),
        secret_keys.google_client_id
    )
    return idinfo

def verify_id_token_form_uri(uri):
    flow.fetch_token(authorization_response=uri)
    return verify_id_token(flow.credentials)




class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: get_user(request))

@app.route('/google/login/callback', methods = ['POST', 'GET'])
def login_scocial():
    if request.method == 'GET':

    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)'''