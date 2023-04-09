import pyrebase

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

#saving the video in the database and returning the url of the video
def save_video(file, name, genre,user_id):
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    db = firebase.database()
    storage.child("Videos/"+file.filename).put(file)
    print("file saved in database successfully")
     # start the upload task in the background
    download_url = storage.child("Videos/"+file.filename).get_url(None)
    print(download_url)
    # store the download URL in Realtime Database
    data={"Name": name,"Genre":genre,"Url":download_url, 'user_id': user_id}
    db.child('Videos_Data').push(data)
    print("successfully entered the video details in realtime database")
    if download_url!=0:
        return download_url
    else:
        return 0
    