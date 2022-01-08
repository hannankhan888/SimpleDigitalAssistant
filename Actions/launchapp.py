#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2022, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"

import os


def launch_app(program_name: str) -> str:
    try:
        first_word = program_name.split(' ', 1)[0]
        app_name = program_name.split(' ', 1)[1]
        if first_word == "Open" or "Launch":
            os.system(app_name)
        return f"opening {app_name}."
    except IndexError:
        print("The application cannot be found or opened.")
        return "I could not find that application."


if __name__ == "__main__":
    # TODO: Still has some bugs. Try to make it so that it can open a program
    # if the path is stored as a var, like this:
    # dict = { "chrome":"C:/Users/HannanKhan/Chrome.exe", "notepad":"C...}
    while True:
        launch = input("Enter the application you would like to launch: ")
        launch_app(launch)
