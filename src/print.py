def printIdented(str, ident=0, end='\n'):
    print(f'{"     " * ident}{str}', end=end)


def printJson(json, ident=0):
    print('{')
    for key, value in json.items():
        printIdented(f'{key}: ', ident+1, '')
        if (isinstance(value, dict)):
            printJson(value, ident+1)
        else:
            print(value, end='')
        
        last = list(json)[-1] != key
        print(',' if last else '')

    printIdented('}', ident, '')