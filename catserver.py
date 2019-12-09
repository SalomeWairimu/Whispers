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
import uuid

from audio_processing import *
from cloud.integrated import *

audios = ["audios/cat1.wav"]

# from server.py
language = 'en'

HOST = '129.105.10.237'  # Standard loopback interface address (localhost) 10.0.0.123 
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
                            qst = audio_to_text("audios/question.wav")
                            print(qst)
                            if qst is None:
                                sound_played = False
                                break
                            play_answer(qst)
                            
       
# get_distance()

cat_audio_questions = {"cat1.wav":["What was fascinating about the cat?", "What is a distinguishing feature about the cat?", "What do you like about the cat?", "What is interesting about the cat?"], 
"cat2.wav": ["What materials were used?", "How was the cat created?"], "cat3.wav": ["What strikes you about the painting?", "What is interesting about the design of the painting?", "What does the circularity of the image remind you of?"]}

def post_audios_from_server_to_cloud():                      
    for i in range(1,4):
        cat_file_name = "cat"+str(i)+".wav"
        path = "audios/" + cat_file_name
        rpid = hex(uuid.getnode())
        postToCloud(path, str(hash((i,rpid))), rpid, cat_audio_questions[cat_file_name], cat_file_name)

# post_audios_from_server_to_cloud()
# print(retrieveByRasberryPiId(hex(uuid.getnode())))

# downloadFile( 
# print(retrieveAudioFileByAudioId("-138064170"))
# play_answer("What was fascinating about the cat?")

#postToCloud("audios/cat1.wav", str(hash((1,"0xb827eb554f09"))), "0xb827eb554f09", ["What was fascinating about the cat?", "What is a distinguishing feature about the cat?"], "cat1.wav")
# print(retrieveByRasberryPiId("0xb827eb554f09"))

# downloadFile("cat1.wav")