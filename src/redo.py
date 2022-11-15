import re
import json
from db import exec
from init import init


def getLog():
    log = dict()
    try:
        with open('../files/entradaLog', 'r', encoding='utf-8') as file:
            for line in file:
                line = re.sub('\n|\r', '', line).strip()

                if (re.match('^<start .+>', line)):
                    transaction = re.sub('<start|>', '', line).strip()
                    log[transaction] = [{
                        'type': 'start'
                    }]

                elif (re.match('^<commit .+>', line)):
                    transaction = re.sub('<commit|>', '', line).strip()
                    log[transaction].append({
                        'type': 'commit'
                    })

                elif (re.match('^<CKPT .+>', line)):
                    transactions = re.sub('<CKPT|>|\\(|\\)| ', '', line).split(',')
                    for transaction in transactions:
                        log[transaction].append({
                            'type': 'checkpoint'
                        })

                elif (re.match('^<.+,.+,.+,.+,.+>', line)):
                    args = re.sub('<|>| ', '', line).strip().split(',')
                    log[args[0]].append({
                        'type': 'change',
                        'id': args[1],
                        'col': args[2],
                        'old': args[3],
                        'new': args[4]
                    })

                else:
                    if (not re.match('^\s*$|<crash>', line)):
                        print('Erro ao ler arquivo de log. Entrada inválida: ' + line)

    except Exception as e:
        print('Erro ao ler arquivo de log. ' + str(e))
        exit()
    return log


def redo():
    init()
    print(json.dumps(getLog(), indent=4, sort_keys=True))


if __name__ == '__main__':
    redo()
