import pyautogui as autogui
import time

# Test pyautogui hotkey press independently
autogui.hotkey('win', 'j')
print("Simulated key press: Win + J")
time.sleep(2)