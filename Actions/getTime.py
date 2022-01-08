#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2022, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"

from datetime import datetime


def get_time(command: str) -> str:
    today = datetime.now()
    if ("date" in command) and ("time" in command):
        return today.strftime("%A %B %d, %Y, %I:%M %p")
    elif "time" in command:
        return today.strftime("%I:%M %p")
    elif "date" in command:
        return today.strftime("%A %B %d, %Y")
    elif "day" in command:
        return today.strftime("%A")


def main():
    print(get_time("whats the date and time"))
    print(get_time("what is today's date"))
    print(get_time("what time is it"))
    print(get_time("what is the current time"))
    print(get_time("what day is it today"))


if __name__ == '__main__':
    main()
