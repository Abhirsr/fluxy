import os
import re
import struct
import webbrowser
from hugchat import hugchat
from playsound import playsound
import eel
from engine.config import ASSISSTANT_NAME
from engine.command import *
import pywhatkit as kit
from engine.db import *
from engine.helper import extract_yt_term
import speech_recognition as sr
import pyaudio
import pyautogui as autogui

#playing assistant sound
@eel.expose
def playassisstantsound():
    music_dir = "C:\\Users\\abhin\\OneDrive\\Desktop\\fluxy\\www\\assets\\audio\\game-start-6104.mp3"
    playsound(music_dir)


def opencommand(query):
    query = query.replace(ASSISSTANT_NAME,"")
    query = query.replace("open","")
    query.lower()
 
    #strip is used to remove spaces between the words
    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                        
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")
    
    
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

import eel
import pyaudio
import struct
import speech_recognition as sr

def hotword():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    keywords = ["hey ram"]

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for hotword...")

            while True:
                audio = recognizer.listen(source)
                try:
                    detected_text = recognizer.recognize_google(audio)
                    if any(keyword in detected_text.lower() for keyword in keywords):
                        print(f"Hotword detected: {detected_text}")

                        if "hey ram" in detected_text.lower():
                            print("hey ram hotword detected")
                            autogui.keyDown("win") 
                            autogui.press("j")
                            time.sleep(2)
                            autogui.keyUp("win")
                            print("Proceeding to microphone operation...")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                   pass

    except Exception as e:
        print(f"Error: {e}")

#chatbot for my assisstant

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

