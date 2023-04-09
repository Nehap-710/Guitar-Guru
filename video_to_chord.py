import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import tempfile
import pyrebase



def rescale_frame(frame, percent=100):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def keras_process_image(img):
    image_x, image_y = 200, 200
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img


def generate_chord_sheet(chords):
    count = 0
    prev_item = None
    str_chord = " "
    for chord in chords:
        if chord == prev_item:
            count = count + 1
        else:
            if prev_item is not None:
                str_chord= str_chord + "Play Chord "+str(prev_item)+" for "+str(count)+" secs" +"\n"
                print(f"Play Chord {prev_item} for {count} secs")
                count = 1
            else:
                count =1
            
            prev_item = chord
    str_chord = str_chord + "Play Chord "+str(prev_item)+" for "+str(count)+" secs" +"\n"
    print(f"Play Chord {prev_item} for {count} secs")
    
    return str_chord

#for getting the video and detecting chords
def process_video_for_chordsheet(filename):
    print(filename)
    global chord_sheet
    global cap
    image_x, image_y = 200, 200
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    model = load_model('guitar_learner_final.h5')
    chord_dict = {0: 'A', 1: 'C', 2: 'F', 3: 'G',4: 'NA'}
    chord_sheet = []
    
    hands = mp_hands.Hands(
        min_detection_confidence=0.7, min_tracking_confidence=0.7)
    hand_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=5)
    hand_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=10, circle_radius=10)
    pic_no = 0
    flag_start_capturing = False
    frames = 0
    # your code to process the video goes here
    cap = cv2.VideoCapture(str(filename))
    print("Started Capturing")
    while True:
        ret, image = cap.read()
        if not ret:
            break
        else:
            image = cv2.flip(image,1)
            image_orig = cv2.flip(image,1)
            image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
            results_hand = hands.process(image)
            #image.flags.writable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results_hand.multi_hand_landmarks:
                for hand_landmarks in results_hand.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image = image,
                        landmark_list = hand_landmarks,
                        connections = mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec = hand_landmark_drawing_spec,
                        connection_drawing_spec = hand_connection_drawing_spec)
            res = cv2.bitwise_and(image, cv2.bitwise_not(image_orig))
            
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            ret, th1 = cv2.threshold(gray, 25, 225, cv2.THRESH_BINARY)
            contours, heirarchy = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours)>0:
                contours = sorted(contours, key=cv2.contourArea)
                contour = contours[-1]
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                save_img = gray[y1:y1 + h1, x1:x1 + w1]
                save_img = cv2.resize(save_img, (image_x, image_y))
                pred_probab, pred_class = keras_predict(model, save_img)
                if pred_class == 0:
                    print("Chord: A")
                    chord_sheet.append("A")
                elif pred_class == 1:
                    print("Chord: C")
                    chord_sheet.append("C")
                elif pred_class == 2:
                    print("Chord: F")
                    chord_sheet.append("F")
                elif pred_class == 3:
                    print("Chord: G")
                    chord_sheet.append("G")
                elif pred_class == 4:
                    print("Chord: No Chord")
                    chord_sheet.append("No Chord")
                else:
                    print(pred_class,pred_probab)
                
                cv2.putText(image, str(chord_dict[pred_class]), (x1 + 50, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 9)
                ret, buffer = cv2.imencode('.jpg', image)
                image = buffer.tobytes()
                if not cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    yield(b'--frame\r\n'
                          b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
                else:
                    print('Video Completed')
                    cap.release()
            else:
                print("OPPS!!! ISUUE")
                chord_sheet.append("NO Chord")
    cap.release()

#for saving the chordhseet generated from the video
def chord_sheet_to_file_link_video(user_id,filename,name,genre):
    cap.release()
    cv2.destroyAllWindows()
    global chord_sheet
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
    print("inside video to chord sheet linking")
    firebase = pyrebase.initialize_app(config)
    chord_string = " "
    for chord in chord_sheet:
        chord_string += chord + " -> "
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
        file.write(chord_string)
        file_path = file.name
    storage = firebase.storage()
    storage.child("ChordSheets/"+name).put(file_path)
    download_url = storage.child("ChordSheets/"+name).get_url(None)
    db = firebase.database()
    data = {'Name': name, 'Genre': genre, 'Chordsheet link':download_url, 'User ID': user_id}
    db.child("ChordSheets").push(data)
    print("Sucessfully pushed chord sheet file into realtime database")
    print(download_url)
    return download_url



