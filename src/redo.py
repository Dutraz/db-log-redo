import re
import json
from db import exec
from init import init
from file_read_backwards import FileReadBackwards


def getLog():
    # Transações e uma lista suas respectivas alterações
    log = dict()
    # Flag indicando se já foi feito checkpoint
    ckpt = False
    # Lista com todos as transações não salvas pelos checkpoints
    redo = set()

    try:
        with FileReadBackwards('../files/entradaLog', encoding='utf-8') as file:
            for line in file:
                line = re.sub('\n|\r', '', line).strip()

                # COMMIT
                if (re.match('^<commit .+>', line)):
                    transaction = re.sub('<commit|>', '', line).strip()

                    # Add transação ao log se não estiver E:
                    # - Ainda não houve checkpoint
                    # - Não foi salva em algum checkpoint
                    if (transaction not in log and (ckpt == False or transaction in redo)):
                        log[transaction] = list()

                # CHECKPOINT
                elif (re.match('^<CKPT\s*\\(.*\\)\s*>', line)):
                    transactions = re.sub('<CKPT\s*\\(|\\)\s*>| ', '', line)
                    ckpt = True
                    redo = set()
                    # Atualiza a lista de transações não salvas
                    if transactions:
                        for transaction in transactions.split(','):
                            redo.add(transaction)

                # UPDATE
                elif (re.match('^<.+,.+,.+,.+,.+>', line)):
                    args = re.sub('<|>| ', '', line)
                    [transaction, id, col, old, new] = args.split(',')

                    # Add registro ao log da transação se foi commitada E:
                    # - Ainda não houve checkpoint 
                    # - Não foi salva em algum checkpoint
                    if (transaction in log and (ckpt == False or transaction in redo)):
                        log[transaction].append({
                            'id': id,
                            'col': col,
                            'old': old,
                            'new': new
                        })
                
                # START
                elif (re.match('^<start .+>', line)):
                    transaction = re.sub('<start|>', '', line).strip()
                    # Se chegou ao início da transação não precisa mais buscar por ela
                    redo.discard(transaction)

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


def redo():
    init()
    print(json.dumps(getLog(), indent=4, sort_keys=True))


if __name__ == '__main__':
    redo()
