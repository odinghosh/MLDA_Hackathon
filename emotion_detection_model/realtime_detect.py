import  cv2
import timeit 
import datetime;
import time
import numpy as np
from tensorflow.keras.models import load_model
from collections import Counter 
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

model_top = load_model('3cls_224_ConfHappySur_Color_newimg.h5')

EMOTION_DICT = {1: 'happy', 0: 'confused', 2: 'surprise'}

cred = credentials.Certificate("./service_account.json")
firebase_admin.initialize_app(cred)

store = firestore.client()

docRef = store.collection(u'lectures/lecture1/students').document(u'student1')




def return_prediction(path):
    #converting image to gray scale and save it
    #img = cv2.imread(path)
    img = path

    
    #detect face in image, crop it then resize it then save it
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    for (x,y,w,h) in faces:
        face_clip = img[y:y+h, x:x+w]
        img1 = cv2.resize(face_clip, (224,224))
        # cv2.imwrite(path, face_resize)
    
        #read the processed image then make prediction and display the result
        read_image = img1 
        read_image = read_image.reshape(1, read_image.shape[0], read_image.shape[1], read_image.shape[2])

        top_pred = model_top.predict(read_image)
        return top_pred


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

cap = cv2.VideoCapture(0)



text = "None"
confused = False
start = timeit.timeit()
confusedCount = 0
while(True):
    ret, img = cap.read()
   
    font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(img, "Emotion was "+str(text), (5,470), font, 1.0, (117, 255, 51), 2, cv2.LINE_AA)
    # cv2.putText(img, "Hold Q: To Quit", (460,470), font, 0.7, (117, 255, 51), 2, cv2.LINE_AA)

    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    
    for x,y,w,h in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
    
    cv2.imshow("Emotion detector", img) 
    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    # cv2.imwrite(str(run) + "_test.jpg", img)
        
    try:
        pred = return_prediction(img)
        if(pred[0].argmax() == 0):
            if(not confused):
                print('confused')
                docRef.set({'confused': True})
                confused = True
        else:
            if(confused):
                print('not confused')
                docRef.set({'confused': False})
                confused = False
    except:
        pass

    
