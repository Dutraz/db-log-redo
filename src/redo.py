import re
import db
from file_read_backwards import FileReadBackwards


def getLog():
    # Lista com as alterações inconsistentes
    log = list()
    # Flag indicando se já foi feito checkpoint
    ckpt = False
    # Lista com todos as transações não salvas pelos checkpoints
    redo = set()
    # Lista com as transações abertas
    opened = set()

    try:
        with FileReadBackwards('../files/entradaLog', encoding='utf-8') as file:
            for line in file:
                # Remove as quebras de linha da string
                line = re.sub('\n|\r', '', line).strip()

                # COMMIT
                if (re.match('^<commit .+>', line)):
                    transaction = re.sub('<commit|>', '', line).strip()

                    # Add transação à lista do redo se:
                    # - Ainda não houve checkpoint
                    # - Não foi salva em algum checkpoint
                    if (ckpt == False or transaction in redo):
                        opened.add(transaction)

                # CHECKPOINT
                elif (re.match('^<CKPT\s*\\(.*\\)\s*>', line)):
                    transactions = re.sub('<CKPT\s*\\(|\\)\s*>| ', '', line)
                    ckpt = True
                    redo = set()
                    # Atualiza a lista de transações não salvas
                    if transactions:
                        redo = set(transactions.split(','))

                # UPDATE
                elif (re.match('^<.+,.+,.+,.+,.+>', line)):
                    args = re.sub('<|>| ', '', line)
                    [transaction, id, col, old, new] = args.split(',')

                    # Add registro ao log se a transação está aberta e:
                    # - Ainda não houve checkpoint
                    # - Não foi salva em algum checkpoint
                    if (transaction in opened and (transaction in redo or not ckpt)):
                        log.append({
                            'transaction': transaction,
                            'id': id,
                            'col': col,
                            'old': old,
                            'new': new
                        })

                # START
                elif (re.match('^<start .+>', line)):
                    transaction = re.sub('<start|>', '', line).strip()
                    # Se chegou ao início da transação não precisa mais buscar por ela
                    opened.discard(transaction)

                # UNDEFINED
                else:
                    if (not re.match('^\s*$|<crash>', line)):
                        print('Erro ao ler arquivo de log. Entrada inválida: ' + line)

                # END
                if (ckpt and not redo):
                    # Se foi feito checkpoint e não há alterações não salvas, finaliza
                    return log

    except Exception as e:
        print('Erro ao ler arquivo de log. ' + str(e))
        exit()

    return log


def checkValue(id, col, val):
    result = db.exec(f'SELECT {col}={val} from log WHERE id={id}')
    # Caso a tupla não esteja na tabela, retorna None
    if (result == []):
        return None
    return result[0][0]


def redo():
    # Lista de registros consistentes
    consistants = set()
    # Lista com transações e flag da necessidade de redo
    transactions = dict()
    
    log = getLog()
    print(log)

    for change in log:
        if (change['transaction'] not in transactions):
            transactions[change['transaction']] = False

        check = checkValue(change['id'], change['col'].lower(), change['new'])
        if (check != True):
            transactions[change['transaction']] = True
            # Caso a tupla ainda não tenha sido inserida
            if (check == None):
                if (change['col'] == 'A'):
                    db.insert(change['id'], change['new'], 'NULL')
                else:
                    db.insert(change['id'], 'NULL', change['new'])
            # Caso o valor esteja inconsistente
            elif (check == False):
                db.update(change['id'], change['col'].lower(), change['new'])
    
    return transactions


if __name__ == '__main__':
    redo()
