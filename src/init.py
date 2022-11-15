import json
from db import exec


def createTable():
    exec('''
        CREATE TABLE log (
            id SERIAL PRIMARY KEY,
            a integer NOT NULL,
            b integer NOT NULL
        )
        ''')


def dropTable():
    exec('DROP TABLE log')


def insert(a, b):
    exec(f'INSERT INTO log (a, b) VALUES ({a}, {b})')


# Lê o arquivo que contém os valores iniciais do banco
def getMetadados():
    data = None
    try:
        f = open('../files/metadado.json')
        data = json.load(f)['INITIAL']
        f.close()
    except:
        print('Erro ao ler arquivo de metadados.')
        exit()
    return list(zip(data['A'], data['B']))


# Popula a tabela com os valores do arquivo de metadados
def populateTable():
    data = getMetadados()
    for d in data:
        insert(d[0], d[1])


def init():
    dropTable()
    createTable()
    populateTable()


if __name__ == '__main__':
    init()
