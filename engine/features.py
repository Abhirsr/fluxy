import os
import re
import struct
import webbrowser
from playsound import playsound
import eel
from engine.config import ASSISSTANT_NAME
from engine.command import *
import pywhatkit as kit
from engine.db import *
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio
import pyautogui as autogui

#playing assistant sound
@eel.expose
def playassisstantsound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
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
import pvporcupine

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Access key and path for hotword detection
        access_key = 't9Bz4EBgHsDzjwNgNGweTMYKjz1Q3vB4I7luNMIscTgrESR7y3hKEg=='  # Replace with your valid access key
        porcupine = pvporcupine.create(access_key,keyword_paths=["www\\assets\\audio\\hey-ram_en_windows_v3_0_0.ppn"])

        # Initialize PyAudio for audio input stream
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        keywords = ["hey ram"]  # Keywords list (you can extend this if needed)

        # Listen for hotword in the audio stream
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                detected_keyword = keywords[keyword_index]
                print(f"Hotword detected: {detected_keyword}")

                # When the hotword is detected, call JavaScript to update the UI
                if detected_keyword == "hey ram":
                    print("hey ram hotword detected")
                    import pyautogui as autogui
                    autogui.keyDown("win") 
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("win")
                 # Call JavaScript function to update the UI
                    print("Proceeding to microphone operation...")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



