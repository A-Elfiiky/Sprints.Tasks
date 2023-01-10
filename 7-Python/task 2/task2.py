while True:

    Y = (input("Please, Enter the year: (q to quit)  "))
    if Y.lower() == 'q':
        break
    Y = int(Y)
    if ((Y % 4 == 0) and (Y % 100 != 0)) or ((Y % 400 == 0) and (Y % 100 == 0)):
        print("{0} is a leap year".format(Y))
    else:
        print("{0} is not a leap year".format(Y))