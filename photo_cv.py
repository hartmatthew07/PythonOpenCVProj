import os

import cv2
import numpy as numpy
import PySimpleGUI as sg

#CONSTANTS
CASCPATH = 'resources\haarcascade_frontalface_alt.xml'
FACECASCADE = cv2.CascadeClassifier(CASCPATH)

def main():
    sg.theme("DarkAmber")

     # Define the window layout
     
    layout = [
        [sg.Text("Photo Capture OpenCV", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Button("Capture", size=(10,1)),sg.Button("Exit", size=(10, 1))]
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(800, 400))
    
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    ret,frame = cap.read() # return a single frame in variable `frame`

    #THE LOOP
    while True:
        event, values = window.read(timeout=20)

        if event == "Exit" or event == sg.WIN_CLOSED:
            #maybe destroyallwindows() here
            break
        
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = FACECASCADE.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        # Can capture single image if rectangle detects face
        for (x, y, w, h) in faces:
            rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if event == "Capture" and rectangle is not None:
                print('Photo Taken')
                path = 'resources/training_images/'
                cv2.imwrite(os.path.join(path,'pic.jpg'), frame)
                # NOTE: THIS DOESNT WORK FOR ALERT
            #elif event == "Capture" and rectangle is None:
            #    print('No Face Detected') 

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

main()

    #cap.release()