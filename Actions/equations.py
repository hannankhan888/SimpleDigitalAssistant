#!/usr/bin/env python
# -*- coding: utf-8 -*-

# __author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
# __copyright__ = "Copyright 2022, SimpleDigitalAssistant"
# __credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
# __license__ = "MIT"
# __version__ = "1.0"
# __maintainer__ = "Hannan Khan"
# __email__ = "hannankhan888@gmail.com"

from word2number import w2n

operators = {'plus': '+', 'minus': '-', 'addition': '+', 'times': '*', 'multiplied': '*', 'divide': '/',
             'divided': '/'}


def list_to_hyphen_string(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for index, ele in enumerate(s):
        if len(s) - 1 != index:
            str1 = str1 + ele + "-"
        else:
            str1 += ele
        # return string
    return str1


def preprocessed(input_equation):
    # find operators
    # go from left to right putting hyphens on numbers only
    # use a for loop
    equation_list = input_equation.split()
    start_index = 0
    processed_equation = ""
    for index, number in enumerate(equation_list):
        if number in operators.keys():
            left_side = equation_list[start_index:index]
            start_index = index + 1
            processed_equation += list_to_hyphen_string(left_side) + " " + number + " "
        elif len(equation_list) == index + 1:
            last_number = equation_list[start_index:]
            processed_equation += list_to_hyphen_string(last_number)
    return processed_equation


def custom_math(math_equation):
    equation = ""
    eq_str = math_equation
    for number in eq_str.split():
        if number == "by":
            continue
        elif number not in operators.keys():
            equation += str(w2n.word_to_num(number))
        elif number in operators.keys():
            equation += operators.get(number)

    try:
        return eval(equation)
    except SyntaxError:
        return "I didn't understand. You can try rephrasing."


if __name__ == "__main__":
    print(custom_math(preprocessed(
        "eleven million three hundred twenty four thousand five hundred thirty two times fifty five times five times three hundred")))  # 934273890000
    print(custom_math(preprocessed("five times five equal to")))  # 25
    print(custom_math(preprocessed("one plus fifty")))  # 51
    print(custom_math(preprocessed("twenty divided by five")))  # 4
    print(custom_math(preprocessed("ten multiplied by five")))  # 50
    print(custom_math(preprocessed("one minus five times five")))  # -24
    print(custom_math(preprocessed(
        "What is eleven million three hundred twenty four thousand five hundred thirty two times fifty five times five times three hundred")))  # 934273890000
    print(custom_math(preprocessed(
        "What's eleven million three hundred twenty four thousand five hundred thirty two times fifty five times five times three hundred")))  # 934273890000
    print(custom_math(preprocessed(
        "What is eleven million three hundred twenty four thousand five hundred thirty two times fifty five times five times three hundred equal to")))  # 934273890000
    print(custom_math(preprocessed(
        "What's eleven million three hundred twenty four thousand five hundred thirty two times fifty five times five times three hundred equal to")))  # 934273890000
