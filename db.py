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
