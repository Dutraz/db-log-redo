import json

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