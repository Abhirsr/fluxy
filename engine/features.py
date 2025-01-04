from playsound import playsound
import eel

#playing assistant sound
@eel.expose



def playassisstantsound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)