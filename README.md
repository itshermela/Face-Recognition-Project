# Face Recognition System To Aid Visually Impaired Person(VIP) 

This project is made using face-recognition library with hog and opencv.

# Requirements

This model requires latest version of python.
It requires dlib library which is coded in c++ and requires installation of visual studio with developer tools in c++.
All other libraries such as pillow, face-recognition, face-recognition-models, numpy, opencv-python, pip, and scikit-learn also have to be imported.

# What is the functionality?

A Face recognition system is a method of identifying and comparing a digital image with a previously stored data. 
What this Face recognition system does is:-
-Recognize known/trained faces (faces in the dataset) who are infront of the webcam and speaks who he/she is to the visually impaired person.
-When a new person introduces him/herself to the visually impaired person, the system automatically records his/her name in the web microphone and puts it in .wav format file.
-The system then converts the recorded voice into a text file(name of the person) via STT (speech to text).
-And then captures and dynamically saves the face-data of the new person to the dataset by mapping it with the converted text file or name of the person.
-When the newly added face-image of the person
-espeak speech synthesizer will speak the name of the person (by matching it to the recognized face of the person) to the visually impaired person.

# Why is it helpful?
-This Face recognition system is mainly important for problems that are related to VIPs which overcomes face recognition problems faced by them.
-Aims at expanding possibilities to people with vision loss to achieve their full potential in any working environment (especially if it is integrated with eyeglass).
-Increases VIP’s confidence by recognizing a person in seconds.
-Simplifying the life of VIPs and let them be aware of their surroundings.

# Limitations/Challenges
- The major limitaion is lack of integration with hardware tools such as eyeglass so as to make the system fully operatable and portable for the VIPs.
- It cannot be applied to recognize multiple persons at a time.
- It does not fully function in difficult situations in terms of lighting and weather.

# Team Members
* Hermela Getnet
Atsedemariam Bizuneh
Adanu Addis




