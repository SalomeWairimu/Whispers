#!/usr/bin/env python3
import socket
import json
import requests
import time
import pygame
from gtts import gTTS
from difflib import SequenceMatcher
import sys
import math
import struct
import time
import csv
import pyaudio
import wave
import speech_recognition as sr

from audio_processing import *

audios = ["audios/crucifixion1.wav"]

# from server.py
language = 'en'

HOST = '10.0.0.123'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def get_distance():
    sound_played = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("server started")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', conn, ' ', addr)
            while True:
                conn, addr = s.accept()
                data = conn.recv(1024)
                if data:
                    j = json.loads(data.decode())['d']['distance']
                    if j<50 and not sound_played:
                        print("playing piece audios")
                        play_piece_audios(audios)
                        sound_played = True
                        while True:
                            record_qst()
                            qst = get_qst("audios/question.wav")
                            print(qst)
                            if qst is None:
                                sound_played = False
                                break
                            play_answer(qst)
                            
       
#get_distance()

crucifixion_audio_questions = {"crucifixion1.wav": ["Did this crucifixion stand out?", "What is origin of the crucifixion?"],
                               "crucifixion2.wav": ["What strikes you about the crucifixion?", "Is there a funny story about the painting?"],
                               "crucifixion3.wav": ["what interests you about this painting?"],
                               "crucifixion4.wav": ["what can you tell me about the materials used for this painting?", "what is the crucifixion based on?", "what materials were used?","what can you tell me about the gold color used?"],
                               "crucifixion5.wav": ["When was it made?", "What was popular at the time?", "Why was metal used?"],
                               "crucifixion6.wav": ["Who is the artist?", "Who influenced the artist?", "Where did the artist go to school?"]}
def post_audios_from_server_to_cloud():                      
    for i in range(1,7):
        crucifixion_file_name = "crucifixion"+str(i)+".wav"
        path = "audios/" + crucifixion_file_name
        rpid = hex(uuid.getnode())
        postToCloud(path, str(hash((i,rpid))), rpid, crucifixion_audio_questions[crucifixion_file_name], crucifixion_file_name)