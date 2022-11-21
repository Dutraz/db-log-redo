from db import selectAll
from redo import redo
from init import init
from print import printJson
from files import getMetadados

def main():
    init()
    transactions = redo()
    for transaction, status in transactions.items():
        print(f'Transação {transaction}{"" if status else " não"} realizou REDO.')

    initial = list(zip(*getMetadados()))
    final = list(zip(*selectAll()))
    printJson({
        'INITIAL': {
            'A': list(initial[0]),
            'B': list(initial[1])
        },
        'FINAL': {
            'A': list(final[0]),
            'B': list(final[1])
        }
    })

if __name__ == '__main__':
    main()