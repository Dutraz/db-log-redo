### Univeridade Federal da Fronteira Sul - Campus Chapecó
### Ciência da Computação - Banco de Dados II – 2022.2
### Prof. Guilherme Dal Bianco
### Acadêmico: **Pedro Zawadzki Dutra**

---

## Trabalho Prático - LOG

### **Objetivo**: 
Implementar o mecanismo de log Redo/Undo com checkpoint usando o SGBD.

### **Funcionamento**: 
O código, que poderá utilizar qualquer linguagem de programação, deverá ser capaz de ler o arquivo de log (entradaLog) e o arquivo de Metadado e validar as informações no banco de dados através do modelo REDO/UNDO. 
O código receberá como entrada o arquivo de metadados (dados salvos) e os dados da tabela que irá operar no banco de dados.

Exemplo de *tabela do banco de dados*:
|  ID  |  A  |  B  |
|------|-----|-----|
|  01  | 100 |  20 |
|  02  |  20 |  30 |

*Arquivo de Metadado (json)*:

```javascript
{  
    "INITIAL": {
        "A": [20,20],
        "B": [55,30]
    }
}
```

*Arquivo de log* no formato:

<transação, “id da tupla”, ”coluna”, “valor antigo”, “valor novo”>.

### **Exemplo:**
Arquivo de Log: 
```
<start T1>
<T1,1, A,20,500>
<start T2>
<commit T1>
<CKPT (T2)>
<T2,2, A,20,50>
<start T3>
<start T4>
<commit T2>
<T4,1, B,20,100>
```

Saída:
>“Transação T2 realizou REDO”

>“Transação T3 não realizou REDO”

>“Transação T4 não realizou REDO”
 
Imprima as variáveis, exemplo:
```javascript
{  
    "INITIAL": {
        "A": [500,20],
        "B": [20,30]
    }
}
```
---
O checkpoint Redo permite que parte do log já processada seja descartada para evitar o reprocessamento. 

### **Detalhes**:
Funções a serem implementadas:
1. Carregar o banco de dados com a tabela antes de executar o código do log (para zerar as configurações e dados parciais);
2. Carregar o arquivo de log;
3. Verifique quais transações devem realizar REDO/UNDO. Imprimir o nome das transações que irão sofrer Redo. Observem a questão do checkpoint;
4. Checar quais valores estão salvos nas tabelas (com o select) e atualizar valores inconsistentes (update);
5. Reportar quais dados foram atualizados;
6. Seguir o fluxo de execução conforme o método de REDO, conforme visto em aula; 
    