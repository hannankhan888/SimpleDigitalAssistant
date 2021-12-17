import winreg
import re
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# key is the application name (str), value is the rest of the info.
app_results = {}
url1 = 'youtube.com'

for key, value in app_results.items():
    print(key, "===>", value)

command = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "ChromeHTML\\shell\open\\command", 0, winreg.KEY_READ), "")[0]
chrome_path=re.search("\"(.*?)\"", command).group(1)

print(chrome_path)
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(str(chrome_path)))
webbrowser.get('chrome').open_new_tab(url1)

import math
# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get current volume
currentVolumeDb = volume.GetMasterVolumeLevel()
volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
# NOTE: -6.0 dB = half volume !


# Sets current brightness to 50%
def set_brightness(value):
    sbc.fade_brightness(value)

set_brightness(50)

