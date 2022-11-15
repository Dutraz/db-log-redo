from db import exec


def createTable():
    exec('''
        CREATE TABLE log (
            id SERIAL PRIMARY KEY,
            a integer NOT NULL,
            b integer NOT NULL
        );
        ''')


def dropTable():
    exec('DROP TABLE log;')


def init():
    dropTable()
    createTable()


if __name__ == '__main__':
    init()
