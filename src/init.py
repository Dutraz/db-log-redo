import json
import db


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
        db.insert(None, d[0], d[1])


def init():
    db.dropTable()
    db.createTable()
    populateTable()


if __name__ == '__main__':
    init()
