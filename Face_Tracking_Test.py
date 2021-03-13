import tkinter as tk
import cv2
from cv2 import Tracker
from PIL import Image, ImageTk
import numpy as np
from Keyboard import function_maker

cap = cv2.VideoCapture(0)
cap.set(3,1280) #3,480
cap.set(4,720)

cascPath = 'haarcascade_frontalface_default.xml'
facecascade = cv2.CascadeClassifier(cascPath)

window_size = 25

start = 0

app = tk.Tk()

video_frame = tk.Label()
video_frame.pack()


#dumb attempt to do the facetracking myself which was working until I found openCV does it for you
def show_frame():
    global fast
    _, frame = cap.read()
    detected_faces = facecascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(detected_faces) > 0:
        for (x, y, w, h) in detected_faces:
            x_value = x + w/8
            y_value = y + h/8
            feature_face = frame[int(y+h/8):int(y+7*h/8), int(x+w/8):int(x+7*w/8)]
            cv2.rectangle(frame, (int(x_value), int(y_value)), (int(x_value+6*w/8), int(y_value+6*h/8)), (0, 200, 0), 4)
        fast = cv2.ORB_create(fastThreshold=50)
        kp = fast.detect(feature_face, None)
        next_best = (0,0,999999)
        best = (0,0,999999)
        for i, keypoint in enumerate(kp):
            print("Keypoint %d: %s" % (i, keypoint.pt))
            centre_distance = (((3*h/8)-keypoint.pt[1])**(2)+((3*w/8)-keypoint.pt[0])**(2))**(0.5)
            if centre_distance < next_best[2]:
                if centre_distance < best[2]:
                    next_best = best
                    best = (keypoint.pt[0], keypoint.pt[1], centre_distance)
                else:
                    next_best = (keypoint.pt[0], keypoint.pt[1], centre_distance)
        scale_distance = ((best[0]-next_best[0])**(2)+(best[1]-next_best[1])**2)**(0.5)
        print(best)
        print(next_best)
        print(scale_distance)
        print(3*w/8,3*h/8)
        cv2.circle(feature_face, (int(best[0]),int(best[1])),5,(0,255,0),2)
        cv2.circle(feature_face, (int(next_best[0]), int(next_best[1])), 5, (0, 255, 0), 2)
        cv2.circle(feature_face, (int(h/4), int(w/4)), 5, (0,0,255),2)
        feature_face = cv2.drawKeypoints(feature_face,kp, None, color=(255,0,0))
        frame[int(y+h/8):int(y+7*h/8), int(x+w/8):int(x+7*w/8)] = feature_face
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_frame.imgtk = imgtk
    video_frame.configure(image=imgtk)
    video_frame.after(2, show_frame)


def why_am_i_dumb(tracker):
    global start
    _, frame = cap.read()
    if start == 0:
        detected_faces = facecascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in detected_faces:
            x_value = x + w/8
            y_value = y + h/8
            feature_face = frame[int(y+h/8):int(y+7*h/8), int(x+w/8):int(x+7*w/8)]
            cv2.rectangle(frame, (int(x_value), int(y_value)), (int(x_value+6*w/8), int(y_value+6*h/8)), (0, 200, 0), 4)
        start = 1
        if len(detected_faces) > 0:
            tracker = cv2.Tracker(frame,feature_face)
            #a = function_maker(why_am_i_dumb, tracker)
            print('face detected')
        else:
            start = 0
        #start = 0
    else:
        success, boundingBox = tracker.update(frame)
        if success:
            (x,y,w,h) = [int(v) for v in enumerate(boundingBox)]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(frame)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_frame.imgtk = imgtk
    video_frame.configure(image=imgtk)
    a = function_maker(why_am_i_dumb, tracker)

    video_frame.after(2, a)
    #why_am_i_dumb(tracker)

tracker1 = 1
#a = function_maker(why_am_i_dumb, tracker1)
why_am_i_dumb(tracker1)
#show_frame()
app.mainloop()