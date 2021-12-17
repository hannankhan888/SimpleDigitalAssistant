import webbrowser
import winapps

# key is the application name (str), value is the rest of the info.
app_results = {}
for item in winapps.search_installed('chrome'):
    app_results[item.name] = item

url1 = 'youtube.com'

for key, value in app_results.items():
    print(key, "===>", value)

chrome_path = app_results['Google Chrome'].install_location
webbrowser.register('chrome',None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(url1)