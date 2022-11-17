from redo import redo
from init import init

def main():
    init()
    transactions = redo()
    for transaction, status in transactions.items():
        print(f'Transação {transaction}{"" if status else " não"} realizou REDO.')

if __name__ == '__main__':
    main()