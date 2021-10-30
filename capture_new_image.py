import os

import cv2
import face_recognition
import speech_recognition as sr

# Sampling frequency
freq = 44100
m = sr.Microphone()

# Recording duration
duration = 3.5
filename = "recording1.wav"

flag = True
timer = 30
num = 0
parent_directory_path = 'imagefile'

r = sr.Recognizer()
mic = sr.Microphone()

try:
    print("A moment of silence, please...")
    with mic as source:
        r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with mic as source:
            audio = r.listen(source)
        print("Recognizing it...")
        try:
            # recognize speech using Sphinx Speech Recognition
            recorded_sound = r.recognize_sphinx(audio)
            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(recorded_sound).encode("utf-8"))
                break
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(recorded_sound))
                break
        except sr.UnknownValueError:
            print("I did not hear you!")
        except sr.RequestError as e:
            print("Couldn't request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    pass

with open('my_result.txt', mode='w') as file:
    file.write("Recognized text:")
    file.write("\n")
    file.write(recorded_sound)
    print("Exporting process completed!")

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
counter = 2
path = os.path.join(parent_directory_path, 'u%d' % counter)

while os.path.exists(path):
    counter += 1
    path = os.path.join(parent_directory_path, 'u%d' % counter)

    if not os.path.exists(path):
        os.makedirs(path)
        break
    else:
        continue
while True:

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)

    for face_location in face_locations:
        num += 1
        name = recorded_sound
        # Save the image in .jpg format
        cv2.imwrite(str(path) + "/" + name + str(num) + ".jpg", frame)
        cv2.imshow('image', frame)
    k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break
    if num >= 10:  # Take 10 face sample and stop video
        break

# video_capture.release()
# cv2.destroyAllWindows()
