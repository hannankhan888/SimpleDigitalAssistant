#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2022, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"

import requests
from bs4 import BeautifulSoup


def wiki_scrape(command):
    command = command.lower()
    ignore = ["tell me about ", "give me some facts about ", "give a fact about ", "give a fact about ", "what is a ",
              "what is ", "what are ", "who is ", "who are ", "what's an ", "what's a"]

    for phrase in ignore:
        if phrase in command:
            command = command.replace(phrase, "")
            print(command)

    try:
        user_request = command
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
                return bullets.get_text()
        else:
            print(paragraph)
            return paragraph
    except Exception as e:
        print(e)


if __name__ == "__main__":
    wiki_scrape("India")
    wiki_scrape("Tell me about India.")
    wiki_scrape("give me some facts about India")
    wiki_scrape("What is a United States of America")
    wiki_scrape("What is Soviet Union")
    wiki_scrape("Tell me about Artificial Intelligence")
    wiki_scrape("Tell me about Orange")
