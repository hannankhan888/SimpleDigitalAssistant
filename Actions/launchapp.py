#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2022, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"

import os


def launch_app(program_name: str):
    try:
        first_word = program_name.split(' ', 1)[0]
        app_name = program_name.split(' ', 1)[1]
        if first_word == "Open" or "Launch":
            os.system(app_name)
    except:
        print("The application cannot be found or opened.")


if __name__ == "__main__":
    while True:
        launch = input("Enter the application you would like to launch: ")
        launch_app(launch)
