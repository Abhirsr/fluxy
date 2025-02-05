import multiprocessing
import subprocess
from engine.command import *

# To run Jarvis
def startjarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

# To run hotword
def listenHotword():