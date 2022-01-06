#!/usr/bin/env python
# -*- coding: utf-8 -*-

# __author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
# __copyright__ = "Copyright 2022, SimpleDigitalAssistant"
# __credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
# __license__ = "MIT"
# __version__ = "1.0"
# __maintainer__ = "Hannan Khan"
# __email__ = "hannankhan888@gmail.com"

from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def weather_information(city: str):
    """Uses HTML headers to pull weather information from web browser, goes by default web browser. Uses .get() function
     to retrieve data and then uses select() to retrieve certain information from the page such as location and time."""

    weather_str = ""
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # TODO: if the city name doesnt make sense, it will stop at the next line.
    # TODO: implement a try-except.
    try:
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        weather_str = location + " " + time + " " + info + " " + weather + "°F"
    except:
        weather_str = "Sorry I could not find that place. Please try again."
    return weather_str


if __name__ == "__main__":
    print(weather_information(
        "Lewisville" + "weather"))  # Test case for City, output should be: Lewisville, TX Monday 5:00 PM Partly cloudy 77°F
    print(weather_information(
        "Texas" + "weather"))  # Test case for State, output should be: Houston, TX Monday 5:00 PM Cloudy 76°F
    print(weather_information(
        "Ontario" + "weather"))  # Test case for province, output should be: Toronto, ON, Canada Monday 6:00 PM Cloudy 32°F
    print(weather_information(
        "United States" + "weather"))  # Test case for country, output should be: Washington, DC Monday 6:00 PM Cloudy 43°F
    print(weather_information("NYC" + "weather"))  # Test case for abbreviated cities, ex: NYC or LA...ect
    print(weather_information(
        "ASKJDNAKSJNDKAJNDKJANSDLKAJSND" + "weather"))  # Test case for non-existent place

    print(
        weather_information("North America" + "weather"))  # Test case for continent, weather information not available.
