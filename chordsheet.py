import pyrebase

'''For Retrieving the chordhseets'''

def get_chordsheet():
    global config
    config = {
    'apiKey': "AIzaSyCZiE4vt37uxA_sJrl03KAhk0jYKOtl5sU",
    'authDomain': "guitarguru-484be.firebaseapp.com",
    'projectId': "guitarguru-484be",
    'storageBucket': "guitarguru-484be.appspot.com",
    'messagingSenderId': "467197811011",
    'appId': "1:467197811011:web:95286f40bdc0c718c0f7f6",
    'measurementId': "G-Y74QRV7FFZ",
    'databaseURL': "https://guitarguru-484be-default-rtdb.asia-southeast1.firebasedatabase.app"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    items = db.child('ChordSheets').order_by_key().limit_to_last(5).get().val()
    item_homepage = list(reversed(list(items.values())))
    return item_homepage
    
def get_all_chordsheet():
    global config
    config = {
    'apiKey': "AIzaSyCZiE4vt37uxA_sJrl03KAhk0jYKOtl5sU",
    'authDomain': "guitarguru-484be.firebaseapp.com",
    'projectId': "guitarguru-484be",
    'storageBucket': "guitarguru-484be.appspot.com",
    'messagingSenderId': "467197811011",
    'appId': "1:467197811011:web:95286f40bdc0c718c0f7f6",
    'measurementId': "G-Y74QRV7FFZ",
    'databaseURL': "https://guitarguru-484be-default-rtdb.asia-southeast1.firebasedatabase.app"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    items = db.child('ChordSheets').order_by_key().get().val()
    item_homepage = list(reversed(list(items.values())))
    return item_homepage

def get_realtime():
    global config
    config = {
    'apiKey': "AIzaSyCZiE4vt37uxA_sJrl03KAhk0jYKOtl5sU",
    'authDomain': "guitarguru-484be.firebaseapp.com",
    'projectId': "guitarguru-484be",
    'storageBucket': "guitarguru-484be.appspot.com",
    'messagingSenderId': "467197811011",
    'appId': "1:467197811011:web:95286f40bdc0c718c0f7f6",
    'measurementId': "G-Y74QRV7FFZ",
    'databaseURL': "https://guitarguru-484be-default-rtdb.asia-southeast1.firebasedatabase.app"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    items = db.child('Realtime_Chordsheets').order_by_key().get().val()
    item_homepage = list(reversed(list(items.values())))
    return item_homepage

def practice_chordsheet(link):
    global config
    config = {
    'apiKey': "AIzaSyCZiE4vt37uxA_sJrl03KAhk0jYKOtl5sU",
    'authDomain': "guitarguru-484be.firebaseapp.com",
    'projectId': "guitarguru-484be",
    'storageBucket': "guitarguru-484be.appspot.com",
    'messagingSenderId': "467197811011",
    'appId': "1:467197811011:web:95286f40bdc0c718c0f7f6",
    'measurementId': "G-Y74QRV7FFZ",
    'databaseURL': "https://guitarguru-484be-default-rtdb.asia-southeast1.firebasedatabase.app"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    items = db.child('ChordSheets').order_by_key().limit_to_last(5).get().val()
    item_homepage = list(reversed(list(items.values())))
    return item_homepage
    