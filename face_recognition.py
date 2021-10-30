import os
import subprocess
import time

import cv2
import face_recognition
import numpy as np

path = 'imagefile'

images = []
known_face_names = []

# Initialize some variables
face_names = []
count = []
person_name = []
process_this_frame = True
face_locations = []
face_encodings = []

flag = True
timer = 30


def espeak(text: str, pitch: int = 50) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode


def find_file(data_folder_path):
    dirs = os.listdir(data_folder_path)
    for dir_name in dirs:
        if not dir_name.startswith("u"):
            continue
        label = int(dir_name.replace("u", ""))
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            images.append(image)
            known_face_names.append(os.path.splitext(image_name)[0])
    print(known_face_names)


find_file(path)


def find_encodings(images):
    return [face_recognition.face_encodings(img)[0] for img in images]


encode_List_Known = find_encodings(images)
print('Encoding complete')

# Create arrays of known face encodings and their names
known_face_encodings = find_encodings(images)
known_face_names = known_face_names

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

while timer > 0 or flag:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces  and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            person_name = ["Unknown", "kk"]

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                for i in name:
                    if i.isnumeric():
                        person_name = name.split(i)
                        break

                time.sleep(0.985)
                timer -= 5
                print(timer)

                # new face is detected
                # as long as a new face isn't detected the timer will decrease and eventually zero
                # when the timer is zero we wanna reset flag= True so that the loop will run again
                if person_name[0] not in count:
                    timer = 30

                    count.append(person_name[0])
                    print(person_name[0])
                    espeak(person_name[0], 70)

                # face has already been detected
                else:
                    flag = False
            face_names.append(person_name[0])

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, person_name[0], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # timer is zero -- for the while loop to run again, set flag to true
    if timer == 0:
        count.clear()
        flag = True
