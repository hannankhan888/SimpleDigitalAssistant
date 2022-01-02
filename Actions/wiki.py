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
def wiki_scrape(topic_name):
    try:
        user_request = topic_name
        response = requests.get(url="https://en.wikipedia.org/wiki/" + user_request)
        # print(response.status_code)

        soup = BeautifulSoup(response.content, 'lxml')
        title = soup.find(id="firstHeading")
        print(title.string)

        body = soup.find(id="mw-content-text").findAll("p")

        paragraph = body[1].get_text()
        last_char = paragraph[-1]
        list_elements = soup.find(id="mw-content-text").find("ul").findAll("li")

        if len(list_elements) > 0 and len(paragraph.split()) < 15:
            for bullets in list_elements:
                print(bullets.get_text())

        else:
            print(paragraph)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    wiki_scrape("India")