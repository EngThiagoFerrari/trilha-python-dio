# Resolução do Lab Project: Otimizando o Sistema Bancário com Funções Python
## Bootcamp NTT DATA - Engenharia de Dados com Python

### Introdução
O arquivo ***sist_banbancario_2.py*** contém minha solução para o Lab Project: "Otimizando o Sistema Bancário com Funções Python" solicitado no Bootcamp NTT DATA - Engenharia de Dados com Python de acordo com suas regras e atualizando a Versão deste arquivo que pode ser consultado em [***sist_bancario_1.py***](https://github.com/EngThiagoFerrari/trilha-python-dio/tree/solucoes_trilha_python/solucoes_python/sist_bancario_1).

### Tecnologia
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  

### Regras do Lab Project  
- As regras de Depósito, Saque e Extrato, ainda respeitam a versão 1 deste projeto.
- Separar as funções existentes de Saque, Depósito e Extrato em funções.
- Criar duas novas funções:
    - Cadastrar usuário (cliente), e
    - Cadastrar nova conta bancária.

#### Separação em funções:  
- Criar funções para todas as operações do sistema.
- Cada função terá uma regra na passagem de argumentos. 
    - Argumentos por posição (pos1, pos2, /,)
    - Argumentos nomeados (*, nome1, nome2) 

#### Função Saque:
- Deve receber os argumentos apenas por nome (keyword only).
- Sugestão de argumentos:
    - saldo, valor, extrato, limite, numero_saques, limite_saques.
- Sugestão de Retorno:
    - Saldo e Extrato


#### Função Depósito:
- Deve receber os argumentos apenas por posição (positional only).
- Sugestão de argumentos:
    - saldo, valor, extrato
- Sugestão de Retorno:
    - Saldo e Extrato

#### Função Extrato:  
- Deve receber os argumentos apenas por posição e nome (positional only e keyword only).
- Argumentos posicionais:
    - saldo
- Argumentos nomeados:
    - extrato

#### Novas Funções:
- Obrigatório: Criar duas novas funções:
    - Criar novo usuário
    - criar conta corrente
- Mais funções podem ser inseridas (não obrigatório)
    - Ex.: Listar Contas

#### Função Criar usuário (cliente)
- O programa deve armazenar os usuários em uma lista.
- um usuário é composto por: nome, data de nascimento, CPF e endereço.
- O endereço é uma string com formato: logradouro, número - bairro - cidade/sigla estado
- Deve ser armazenado somente os números do CPF
- Não deve ser permitido cadastrar mais de 1 usuário com o mesmo CPF

#### Função Criar Conta Corrente
- O programa deve armazenar as contas em uma lista.
- Uma conta é composta por: agência, número da conta e usuário.
- O número da conta é sequencial, iniciando em 1.
- O número da agência é fixo: "0001"
- Um usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.


### Melhorias implementadas
- Atendiemnto aos requisitos listados nas regras deste desafio:
    - Operações separadas em diferentes funções
    - Incluídas as funções:
        - Cadastrar Novo Cliente;
        - Cadastrar Nova Conta;
        - Listar Contas

- Limpeza do terminal a cada operação para garantir maior clareza no entendimento das informações exibidas ao usuário.