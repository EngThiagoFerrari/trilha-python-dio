menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

#A v1 do projeto trabalha apenas com 1 usuario.
#Depósito: Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato.
#Saque: O sistema deve permitir realizar 3 saques diários com limite máximo de 500/ saque. Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mensagem informando que náo será possível sacar o dinheiro por falta de saldo. todos os sques devem ser armazenados em uma variável e exibidos na operação de extrato.
#Extrato: deve listar todos os depósitos e saqus realizados na conta. No fim da listagem deve ser exibido o saldo atual da conta. Os valores devem ser exibidos utilizando o formato R$ xxx.xx, exemplo: 1500.45 = R$ 1500.45

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    # MENU INICIAL
    opcao = input(menu)

    # OPERAÇÃO DEPÓSITO
    if opcao == "d":
        while True:
            deposito = input("Informe o valor do depósito ou tecle 'q' para cancelar a operação e voltar ao menu inicial: ").lower()
            try:
                #incluído o método try/ except para lidar com o erro de valor, mantendo o loop até que um valor válido seja inserido
                if deposito == "q":
                    break

                elif float(deposito) > 0:
                    deposito = float(deposito)
                    saldo += deposito
                    extrato += "  Crédito".ljust(0) + f"R$ {deposito:.2f}\n".rjust(49 - len("  Crédito"))
                    print(f"\nVocê depositou: R$ {deposito:.2f}")
                    print(f"\nSeu saldo atual é de: R$ {saldo:.2f}")
                    break

            except ValueError:
                print("Insira um valor de depósito válido ou a tecla 'q' para cancelar a operação.")

    
    # OPERAÇÃO SAQUE
    elif opcao == "s":
        if numero_saques < LIMITE_SAQUES: #verificando se o número de saques supera o limite antes de permitir ao usuário inserir qualquer valor
            
            while True:
                saque = input("Informe o valor do saque ou tecle 'q' para cancelar a operação e voltar ao menu inicial: ").lower()
                try:
                    #incluído o método try/ except para lidar com o erro de valor, mantendo o loop até que um valor válido seja inserido
                    if saque == "q":
                        break

                    elif float(saque) >= saldo: #checando se há saldo suficiente na conta
                        print("Falha na operação! Você não tem saldo suficiente.")

                    elif float(saque) > limite: #checando se o saque supera o limite por saque
                        print(f"Falha na operação! O valor indicado supera seu limite de R$ {limite:.2f} por saque.")

                    elif float(saque) > 0 and float(saque) <= limite:
                        saque = float(saque)
                        saldo -= saque
                        extrato += "  Débito".ljust(0) + f"R$ {saque:.2f}\n".rjust(49 - len("  Débito"))
                        numero_saques += 1
                        print(f"\nVocê sacou: R$ {saque:.2f}")
                        print(f"\nSeu saldo atual é de: R$ {saldo:.2f}")
                        break

                except ValueError:
                    print("Insira um valor de depósito válido ou a tecla 'q' para cancelar a operação.")

        else:
            print(f"Falha na operação! Você atingiu o limite de {LIMITE_SAQUES} saques diários.")


    elif opcao == "e":
        largura_extrato = 50
        print("EXTRATO".center(largura_extrato, "="))
        print("Não foram realizadas movimentações" if not extrato else extrato)
        print("-" * largura_extrato)
        print("  Saldo total:".ljust(0) + f"R$ {saldo:.2f}".rjust(48 - len("  Saldo total:")))
        print("=" * largura_extrato)
    
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

print("\nObrigado pela preferência. Tenha um bom dia!\n")
