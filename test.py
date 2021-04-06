def equationSetup(eqString, xlist):
    parsedEquation = list(eqString)
    pointer = 0
    while pointer < len(eqString):
        if parsedEquation[pointer] == '^':
            parsedEquation[pointer] = '**'
        if parsedEquation[pointer].isdigit() and (parsedEquation[pointer+1] == 'x' or parsedEquation[pointer+1] == '('):
            parsedEquation.insert(pointer+1,'*')
        if parsedEquation[pointer] == ')' and (parsedEquation[pointer+1] == 'x' or parsedEquation[pointer+1].isdigit()):
            parsedEquation.insert(pointer+1,'*')
        pointer += 1

    finalEquation = ''.join(parsedEquation)
    print(finalEquation)
    
    return [eval(finalEquation) for x in xlist]


# PEMDAS
something = input('something')
print(equationSetup(something, range(-10,10)))


# print([eval('2*(x**3)+(x**2)') for x in range(-10,10)])