from word2number import w2n
def math(math_equation):
    operators = {'plus': '+', 'minus': '-', 'addition': '+', 'times': '*', 'multiplied': '*', 'divide': '/',
                 'divided': '/'}

    equation = ""
    eq_str = math_equation
    for number in eq_str.split():
        if number == "by":
            continue
        elif number not in operators.keys():
            equation += str(w2n.word_to_num(number))
        elif number in operators.keys():
            equation += operators.get(number)

    return eval(equation)

if __name__ == "__main__":
    print(math("nine plus five plus twenty plus three minus five divided by two minus three times ten")) #4.5
    print(math("nine times five times eleven times two minus three")) #987
    print(math("one million five hundred thousand two hundred forty-three times fifty five")) #60788365 failed TODO: Fix big number calculation


