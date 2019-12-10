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

HOST = '129.105.209.248'  # Standard loopback interface address (localhost) 10.0.0.123 
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def get_distance():
    sound_played = False
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()
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
                        print("dist is ", j)
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
                            play_answer(qst+"?")

                            
       
get_distance()

cat_audio_questions = {"cat1.wav":["What was fascinating about the cat?", "What is a distinguishing feature about the cat?", "What do you like about the cat?", "What is interesting about the cat?", "What is compelling about the abstraction?"],
                       "cat2.wav": ["What materials were used?", "What did the painter use to creat the painting?", "How was the cat created?"],
                       "cat3.wav": ["What strikes you about the painting?", "What is interesting about the design of the painting?", "What does the circularity of the image remind you of?"],
                       "cat4.wav": ["Where is the artist from?"],"cat5.wav":["When was this painting made?"], "cat6.wav":["How was the painting made?"],
                       "cat7.wav":["What is the meaning of the painting?", "What symbolism is used in this painting?", "What do the colors represent"]}

def post_audios_from_server_to_cloud():                      
    for i in range(1,8):
        cat_file_name = "cat"+str(i)+".wav"
        path = "audios/" + cat_file_name
        rpid = hex(uuid.getnode())
        postToCloud(path, str(hash((i,rpid))), rpid, cat_audio_questions[cat_file_name], cat_file_name)

# post_audios_from_server_to_cloud()

# play_answer("What symbolism is used in this painting")
