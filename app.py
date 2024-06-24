import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3

engine = pyttsx3.init()
engine.say("Welcome to Real-Time gesture Vacalizer")
engine.runAndWait()

# Initialize the hand detector and classifier
detector = HandDetector(maxHands=1)
classifier = Classifier("/Users/krish/OneDrive/Desktop/App/major project/SLD/Model/keras_model.h5",
                        "/Users/krish/OneDrive/Desktop/App/major project/SLD/Model/labels.txt")
offset = 20
imgSize = 300

labels = ["Hello", "", "No", "Okay", "Please", "Thank you", "Yes"]

# Streamlit interface

def main():
    # Placeholder for the video feed
    video_placeholder = st.empty()

    # Video capture
    cap = cv2.VideoCapture(0)


    while True:
        success, img = cap.read()
        if not success:
            st.write("Failed to capture video")
            break

        imgOutput = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]

            if imgCrop.size > 0:  # Make sure imgCrop is not empty
                imgCropShape = imgCrop.shape
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)

                # engine.say(labels[index])
                # engine.runAndWait()

                cv2.rectangle(imgOutput, (x-offset, y-offset-70), (x-offset+400, y-offset+60-50), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                cv2.rectangle(imgOutput, (x-offset, y-offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)

        # Convert the image color format from BGR to RGB
        imgOutput = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)

        # Display the image in the Streamlit app
        video_placeholder.image(imgOutput, channels='RGB')


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()