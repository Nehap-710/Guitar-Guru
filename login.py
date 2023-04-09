from lib2to3.pgen2 import token
from google.oauth2 import id_token
import pyrebase

config = {
    'apiKey': "AIzaSyCZiE4vt37uxA_sJrl03KAhk0jYKOtl5sU",
    'authDomain': "guitarguru-484be.firebaseapp.com",
    'projectId': "guitarguru-484be",
    'storageBucket': "guitarguru-484be.appspot.com",
    'messagingSenderId': "467197811011",
    'appId': "1:467197811011:web:95286f40bdc0c718c0f7f6",
    'measurementId': "G-Y74QRV7FFZ",
    'databaseURL': ''
}

def login_user(email,password):
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email,password)
        id_token = user['localId']
        return id_token
    except:
        return 0

def google_login(id):
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_custom_token(id)
        id_token = user['localId']
        return id_token
    except:
        return 0