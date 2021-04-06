def equationSetup(eqString, xlist):
    parsedEquation = list(eqString)
    pointer = 0
    eqLen = len(parsedEquation)
    while pointer < eqLen:
        print(pointer, eqLen)
        if parsedEquation[pointer] == '^':
            parsedEquation[pointer] = '**'
        try:
            if parsedEquation[pointer].isdigit() and (parsedEquation[pointer+1] == 'x' or parsedEquation[pointer+1] == '('):
                parsedEquation.insert(pointer+1,'*')
            if parsedEquation[pointer] == ')' and (parsedEquation[pointer+1] == 'x' or parsedEquation[pointer+1].isdigit()):
                parsedEquation.insert(pointer+1,'*')
        except:
            pass
        eqLen = len(parsedEquation)
        pointer += 1

    finalEquation = ''.join(parsedEquation)
    print(finalEquation)
    
    return [eval(finalEquation) for x in xlist]


# PEMDAS

something = '1+x+1(x**2+5*x^3)'
print(equationSetup(something, range(-10,10)))


# print([eval('2*(x**3)+(x**2)') for x in range(-10,10)])