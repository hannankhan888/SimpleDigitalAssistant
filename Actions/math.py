from word2number import w2n

operators = {'plus': '+', 'minus': '-', 'addition': '+', 'times': '*', 'multiplied': '*', 'divide': '/',
                  'divided': '/'}

equation = ""
eq_str = "two plus one times five minus one divide two"
for number in eq_str.split():
    if number not in operators.keys():
        equation+=str(w2n.word_to_num(number))
    elif number in operators.keys():
        equation+=operators.get(number)

print(eval(equation))