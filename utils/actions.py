import winreg
import re
import webbrowser
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
