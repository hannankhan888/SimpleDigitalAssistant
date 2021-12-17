import winreg
import re
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import os

input_str_1 = "Open Google Chrome"
input_str_2 = "Open Youtube"
input_str_3 = "Open Notepad"

url = 'youtube.com'

command = \
    winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "ChromeHTML\\shell\open\\command", 0, winreg.KEY_READ),
                        "")[0]
chrome_path = re.search("\"(.*?)\"", command).group(1)

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(str(chrome_path)))


def open_url(value):
    webbrowser.get('chrome').open_new_tab(value)


open_url('youtube.com')
open_url('mail.google.com')

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get current volume
currentVolumeDb = volume.GetMasterVolumeLevel()
volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)


# NOTE: -6.0 dB = half volume


# Sets current brightness to 50%
def set_brightness(value):
    sbc.fade_brightness(value)


set_brightness(50)

# Asks user if they want to shut down computer
shutdown = input("Do you wish to shutdown your computer ? (yes / no): ")

if shutdown == 'no':
    exit()
else:
    os.system("shutdown /s /t 1")

