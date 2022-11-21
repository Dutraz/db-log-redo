import files
import db
from db import exec


# Popula a tabela com os valores do arquivo de metadados
def populateTable():
    data = files.getMetadados()
    for d in data:
        db.insert(None, d[0], d[1])


def init():
    db.dropTable()
    db.createTable()
    populateTable()


if __name__ == '__main__':
    init()
