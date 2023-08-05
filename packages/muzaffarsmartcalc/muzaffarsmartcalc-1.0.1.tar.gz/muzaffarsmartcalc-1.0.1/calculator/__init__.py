

def calc(t, num1, num2):

    # t = input("Ishora kiriting (ex: + - / * % ^)>>> ")

    # num1 = input("1-sonni kiriting kiriting >>> ")
    # num2 = input("2-sonni kiriting kiriting >>> ")


    if t == "+":

        result = num1 + num2
        print(int(result))

    if t == "-":

        result = num1 - num2
        print(int(result))

    if t == "/":

        result = num1 / num2
        print(int(result))

    if t == "*":

        result = num1 * num2
        print(int(result))

    if t == "%":

        result = num1 % num2
        print(int(result))

    if t == "^":

        result = num1 ** num2
        print(int(result))

def auth():

    print("""
    Author: Muzaffar Sharofiddinov
    """)
        