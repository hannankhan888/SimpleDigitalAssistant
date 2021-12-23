import time
import winreg
import re
import webbrowser
from ctypes import cast, POINTER

import gtts
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from dateutil.parser import parse
import concurrent.futures
import pandas as pd
from word2number import w2n
from gtts import gTTS
import os
from playsound import playsound
import winsound
import multiprocessing
from pydub import AudioSegment



curr_time_date = datetime.now()
current_time = curr_time_date.strftime("%H:%M:%S")
hours = curr_time_date.strftime("%H")
minutes = curr_time_date.strftime("%M")
AM_PM = curr_time_date.strftime("%p")
language = 'en'

output = gTTS(text=str('The time is'+hours + " " + minutes + " " + AM_PM + " "), lang=language, slow=False)
output.save("timeanddate.mp3")
sound = AudioSegment.from_mp3("timeanddate.mp3")
sound.export("timeanddate.wav", format="wav")
winsound.PlaySound("timeanddate.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
# print ("Current date and time = %s" % curr_time_date)

# # input_str_1 = "Open Google Chrome"
# # input_str_2 = "Open Youtube"
# # input_str_3 = "Open Notepad"
# #
# # url = 'youtube.com'
# #
# # command = \
# #     winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "ChromeHTML\\shell\open\\command", 0, winreg.KEY_READ),
# #                         "")[0]
# # chrome_path = re.search("\"(.*?)\"", command).group(1)
# #
# # webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(str(chrome_path)))
# #
# #
# # def open_url(value):
# #     webbrowser.get('chrome').open_new_tab(value)
# #
# #
# # open_url('youtube.com')
# # open_url('mail.google.com')
# #
# # devices = AudioUtilities.GetSpeakers()
# # interface = devices.Activate(
# #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# # volume = cast(interface, POINTER(IAudioEndpointVolume))
# # # Get current volume
# # currentVolumeDb = volume.GetMasterVolumeLevel()
# # volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
# #
# #
# # # NOTE: -6.0 dB = half volume
# #
# #
# # # Sets current brightness to 50%
# # def set_brightness(value):
# #     sbc.fade_brightness(value)
# #
# #
# # set_brightness(50)
# #
# # # Asks user if they want to shut down computer
# # shutdown = input("Do you wish to shutdown your computer ? (yes / no): ")
# #
# # if shutdown == 'no':
# #     exit()
# # else:
# #     os.system("shutdown /s /t 1")
# #
#
# # Code for Web Scraping. This is for IMDB
# #
# # MAX_THREADS = 50
# # movie_title_arr = []
# # movie_year_arr = []
# # movie_genre_arr = []
# # movie_synopsis_arr = []
# # image_url_arr = []
# # image_id_arr = []
# #
# #
# # def getMovieTitle(header):
# #     try:
# #         return header[0].find("a").getText()
# #     except:
# #         return 'NA'
# #
# #
# # def getReleaseYear(header):
# #     try:
# #         return header[0].find("span", {"class": "lister-item-year text-muted unbold"}).getText()
# #     except:
# #         return 'NA'
# #
# #
# # def getGenre(muted_text):
# #     try:
# #         return muted_text.find("span", {"class": "genre"}).getText()
# #     except:
# #         return 'NA'
# #
# #
# # def getsynopsys(movie):
# #     try:
# #         return movie.find_all("p", {"class": "text-muted"})[1].getText()
# #     except:
# #         return 'NA'
# #
# #
# # def getImage(image):
# #     try:
# #         return image.get('loadlate')
# #     except:
# #         return 'NA'
# #
# #
# # def getImageId(image):
# #     try:
# #         return image.get('data-tconst')
# #     except:
# #         return 'NA'
# #
# #
# # def main(imdb_url):
# #     response = requests.get(imdb_url)
# #     soup = BeautifulSoup(response.text, 'html.parser')
# #
# #     # Movie Name
# #     movies_list = soup.find_all("div", {"class": "lister-item mode-advanced"})
# #
# #     for movie in movies_list:
# #         header = movie.find_all("h3", {"class": "lister-item-header"})
# #         muted_text = movie.find_all("p", {"class": "text-muted"})[0]
# #         imageDiv = movie.find("div", {"class": "lister-item-image float-left"})
# #         image = imageDiv.find("img", "loadlate")
# #
# #         #  Movie Title
# #         movie_title = getMovieTitle(header)
# #         movie_title_arr.append(movie_title)
# #
# #         #  Movie release year
# #         year = getReleaseYear(header)
# #         movie_year_arr.append(year)
# #
# #         #  Genre  of movie
# #         genre = getGenre(muted_text)
# #         movie_genre_arr.append(genre)
# #
# #         # Movie Synopsys
# #         synopsis = getsynopsys(movie)
# #         movie_synopsis_arr.append(synopsis)
# #
# #         #  Image attributes
# #         img_url = getImage(image)
# #         image_url_arr.append(img_url)
# #
# #         image_id = image.get('data-tconst')
# #         image_id_arr.append(image_id)
# #
# #
# # imageArr = []
# # MAX_PAGE = 51
# # for i in range(0, MAX_PAGE):
# #     totalRecords = 0 if i == 0 else (250 * i) + 1
# #     imdb_url = f'https://www.imdb.com/search/title/?release_date=2020-01-02,2021-02-01&user_rating=4.0,10.0&languages=en&count=250&start={totalRecords}&ref_=adv_nxt'
# #     imageArr.append(imdb_url)
# #
# #
# # def download_stories(story_urls):
# #     threads = min(MAX_THREADS, len(story_urls))
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
# #         executor.map(main, story_urls)
# #
# #
# # # Call the download function with the array of URLS called imageArr
# # download_stories(imageArr)
# #
# # # Attach all the data to the pandas dataframe. You can optionally write it to a CSV file as well
# # movieDf = pd.DataFrame({
# #     "Title": movie_title_arr,
# #     "Release_Year": movie_year_arr,
# #     "Genre": movie_genre_arr,
# #     "Synopsis": movie_synopsis_arr,
# #     "image_url": image_url_arr,
# #     "image_id": image_id_arr,
# # })
# #
# # print('--------- Download Complete CSV Formed --------')
# #
# # movieDf.to_csv('file.csv', index=False)
# # #movieDf.head()
# #
# #
#
#
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # MAX_THREADS = 50
# # TitleofPage = []
# # First_Paragraph = []
# #
# #
# # def getTitleofPage(header):
# #     try:
# #         return header[0].find("h1").getText()
# #     except:
# #         return 'NA'
# #
# #
# # def getFirst_Paragraph(header):
# #     try:
# #         return header[0].find("p").getText()
# #     except:
# #         return 'NA'
# #
# #
# #
# # def main(wikipedia_url):
# #     response = requests.get(wikipedia_url)
# #     soup = BeautifulSoup(response.text, 'html.parser')
# #
# #     # Movie Name
# #     movies_list = soup.find_all("h1")
# #
# #     for movie in movies_list:
# #         header = movie.find_all("h3", {"class": "lister-item-header"})
# #         muted_text = movie.find_all("p", {"class": "text-muted"})[0]
# #
# #
# #         #  Movie Title
# #         movie_title = getMovieTitle(header)
# #         movie_title_arr.append(movie_title)
# #
# #         #  Movie release year
# #         year = getReleaseYear(header)
# #         movie_year_arr.append(year)
# #
# #
# #
# # imageArr = []
# # MAX_PAGE = 51
# # for i in range(0, MAX_PAGE):
# #     totalRecords = 0 if i == 0 else (250 * i) + 1
# #     imdb_url = f'https://www.imdb.com/search/title/?release_date=2020-01-02,2021-02-01&user_rating=4.0,10.0&languages=en&count=250&start={totalRecords}&ref_=adv_nxt'
# #     imageArr.append(imdb_url)
# #
# #
# # def download_stories(story_urls):
# #     threads = min(MAX_THREADS, len(story_urls))
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
# #         executor.map(main, story_urls)
# #
# #
# # # Call the download function with the array of URLS called imageArr
# # download_stories(imageArr)
# #
# # # Attach all the data to the pandas dataframe. You can optionally write it to a CSV file as well
# # movieDf = pd.DataFrame({
# #     "Title": movie_title_arr,
# #     "Release_Year": movie_year_arr,
# # })
# #
# # print('--------- Download Complete CSV Formed --------')
# #
# # movieDf.to_csv('file.csv', index=False)
# # #movieDf.head()
# #
#
#
# # Web scraping Wikipedia
# paras = []
try:
    user_request = input("enter what you want to know: ")
    response = requests.get(url="https://en.wikipedia.org/wiki/" + user_request)
    # print(response.status_code)

    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.find(id="firstHeading")
    print(title.string)

    body = soup.find(id="mw-content-text").findAll("p")

    paragraph = body[1].get_text()
    last_char = paragraph[-1]

    # print(body[2].get_text())
    if last_char != '.':
        print(body[1].get_text())

        language = 'en'
        output = gTTS(text=body[1].get_text(), lang=language, slow=False)

    elif paragraph == "\n":
        paragraph = body[2].get_text()
        last_char = paragraph[-2]
        print(body[2].get_text())
        language = 'en'
        output = gTTS(body[2].get_text(), lang=language, slow=False)
    else:
        last_char = paragraph[-2]
        body2 = soup.find(id="mw-content-text").find("ul").findAll("li")
        for bullets in body2:
            print(bullets.get_text())
            language = 'en'
            output = gTTS(text=bullets.get_text(), lang=language, slow=False)

    output.save("wikiTTS.mp3")
    sound = AudioSegment.from_mp3("wikiTTS.mp3")
    sound.export("wikiTTS.wav", format="wav")
    winsound.PlaySound("wikiTTS.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    input("Press ENTER to stop the audio ")
    winsound.PlaySound(None, winsound.SND_PURGE)




except:
    print("The word was not found")


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele + " "

        # return string
    return str1


# first_operand = listToString(first_number)
# last_operand = listToString(last_number)
# print("first_operand:", first_operand)
# print("last_operand:", last_operand)

def string_to_equation_answer(eq_str: str) -> str:
    operators = {'plus': '+', 'minus': '-', 'addition': '+', 'times': '*', 'multiplied': '*', 'divide': '/',
                 'divided': '/'}
    first_number = None
    last_number = None
    op_idx = None
    last_operand = None

    equation_list = eq_str.split()

    for operator in operators.keys():
        if operator in equation_list:

            if (operator == 'multiplied') | (operator == 'divided'):
                op_idx = equation_list.index(operator)
                first_number = equation_list[0:op_idx]
                last_number = equation_list[op_idx + 2:]
            else:
                op_idx = equation_list.index(operator)
                first_number = equation_list[0:op_idx]
                last_number = equation_list[op_idx + 1:]
            break

    first_operand = listToString(first_number)
    if len(last_number) > 1:
        last_number = string_to_equation_answer(listToString(last_number))
        last_operand = (str(last_number))
        oper = equation_list[op_idx]
        answer = eval(str(w2n.word_to_num(first_operand)) + str(operators[oper]) + str(last_operand))
    else:
        last_operand = listToString(last_number)
        oper = equation_list[op_idx]
        answer = eval(str(w2n.word_to_num(first_operand)) + str(operators[oper]) + str(w2n.word_to_num(last_operand)))

    return answer


eq_str = input("Enter math Equation ")

print(string_to_equation_answer(eq_str))


