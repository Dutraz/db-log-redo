import psycopg2

from config import config


# Conecta ao banco, executa o comando sql e retorna a mensagem do banco de dados
def exec(sql):
    con = None
    result = None
    params = config()

    try:
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute(sql)

        if cur.pgresult_ptr is not None:
            result = cur.fetchall()

        cur.close()
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
        return result


def createTable():
    exec('''
        CREATE TABLE log (
            id SERIAL PRIMARY KEY,
            a integer NOT NULL,
            b integer NOT NULL
        )
        ''')


def dropTable():
    exec('DROP TABLE IF EXISTS log')


def insert(id, a, b):
    if id == None:
        exec(f'INSERT INTO log(a, b) VALUES ({a}, {b})')
    else:
        exec(f'INSERT INTO log VALUES ({id}, {a}, {b})')


def update(id, col, val):
    exec(f'UPDATE log set {col}={val} WHERE id={id}')


def selectAll():
    return exec('SELECT a, b FROM log ORDER BY id')
