from os import system
from time import sleep
import textwrap


def menu():
    system('cls')
    menu = """\n
    ================== MENU =====================
    Escolha a operação desejada.

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [cc]\tCadastrar Nova Conta
    [lc]\tListar Contas
    [nc]\tCadastrar Novo Cliente
    
    [q]\tSair

    => """
    return input(textwrap.dedent(menu)).lower()


def depositar(saldo, extrato, /):
    while True:
        system('cls')
        print("\tOperação selecionada => Depositar")
        deposito = input("\nInforme o valor do depósito ou tecle 'q' para cancelar a operação e voltar ao menu inicial: ").lower()
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
                print(input("Pressione a tecla 'ENTER' para voltar ao MENU"))
                break

        except ValueError:
            print("\nOPERAÇÃO INVÁLIDA!")
            print("\nInsira um valor de depósito válido ou a tecla 'q' para cancelar a operação.")
            sleep(5)

    return saldo, extrato


def sacar(*, saldo, extrato, limite, numero_saques, limite_saques):
    if numero_saques < limite_saques: #verificando se o número de saques supera o limite antes de permitir ao usuário inserir qualquer valor
        while True:
            system('cls')
            print("\tOperação selecionada => Sacar")
            saque = input("\nInforme o valor do saque ou tecle 'q' para cancelar a operação e voltar ao menu inicial: ").lower()
            try:
                #incluído o método try/ except para lidar com o erro de valor, mantendo o loop até que um valor válido seja inserido
                if saque == "q":
                    break

                elif float(saque) >= saldo: #checando se há saldo suficiente na conta
                    print("Falha na operação! Você não tem saldo suficiente.")
                    sleep(3)

                elif float(saque) > limite: #checando se o saque supera o limite por saque
                    print(f"Falha na operação! O valor indicado supera seu limite de R$ {limite:.2f} por saque.")
                    sleep(3)

                elif float(saque) > 0 and float(saque) <= limite:
                    saque = float(saque)
                    saldo -= saque
                    extrato += "  Débito".ljust(0) + f"(R$ {saque:.2f})\n".rjust(49 - len("  Débito"))
                    numero_saques += 1
                    print(f"\nVocê sacou: R$ {saque:.2f}")
                    print(f"\nSeu saldo atual é de: R$ {saldo:.2f}")
                    print(input("Pressione a tecla 'ENTER' para voltar ao Menu."))
                    break

            except ValueError:
                print("Insira um valor de depósito válido ou a tecla 'q' para cancelar a operação.")
                sleep(3)

    else:
        print(f"Falha na operação! Você atingiu o limite de {limite_saques} saques diários.")
        sleep(3)
    
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    system('cls')
    largura_extrato = 50
    print(" EXTRATO ".center(largura_extrato, "="))
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print("-" * largura_extrato)
    print("  Saldo total:".ljust(0) + f"R$ {saldo:.2f}".rjust(48 - len("  Saldo total:")))
    print("=" * largura_extrato)
    print(input("\nPressione a tecla ENTER para voltar ao menu."))
    

def criar_cliente(clientes):
    system('cls')
    print("\tOperação selecionada => Cadastrar novo Cliente")
    cpf = input("Informe o CPF (somente números): ")
    cliente = buscar_cliente(cpf, clientes)

    if cliente:
        print("\nFALHA NA OPERAÇÃO")
        print("\n\nAtenção! Este CPF já está cadastrado.\n")
        sleep(3)
        return
    
    nome = input("inoforme o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla do estado):\n=> ")

    clientes.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereço": endereco,
        })

    print("\nUsuário cadastrado com sucesso!\n")
    print(input("Pressione a tecla 'ENTER' para voltar ao Menu principal."))
    

def buscar_cliente(cpf, clientes):
    filtrar_cliente = [cliente for cliente in clientes if cliente["cpf"] == cpf]
    
    return filtrar_cliente[0] if filtrar_cliente else None


def criar_conta(agencia, numero_conta, clientes):
    system('cls')
    print("\tOperação selecionada => Cadastrar Nova Conta")
    cpf = input("\nInforme o CPF do cliente: ")
    cliente = buscar_cliente(cpf, clientes)

    if cliente:
        print("\nConta criada com sucesso!\n")
        sleep(3)
        return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}
    
    print("\nUsuário não encontrado, o processo de criação de conta foi encerrado!\n")
    sleep(3)


def listar_contas(contas):
    system("cls")
    print("\tOperação selecionada => Listar as contas cadastradas\n")
    if contas:
        print(80 * "=")
        for conta in contas:
            print(textwrap.dedent(f"""
                  Agência:\t{conta["agencia"]}
                  Conta:\t\t{conta["numero_conta"]}
                  Cliente:\t{conta["cliente"]["nome"]}
                  CPF:\t\t{conta["cliente"]["cpf"]}"""))
            print(80 * "-")
        
        print(80 * "=")
        print(input("\nPressione a tecla 'ENTER' para voltar ao menu.\n"))
        return

    print('\nNenhuma conta foi cadastrada!\n')
    sleep(3)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    clientes = []
    contas = []
    

    while True:
        # MENU INICIAL
        opcao = menu()

        # OPERAÇÃO DEPÓSITO
        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
            
        # OPERAÇÃO SAQUE
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(
                saldo = saldo,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        # OPERAÇÃO DE EXIBIR EXTRATO    
        elif opcao == "e":
            exibir_extrato(saldo, extrato = extrato)

        # OPERAÇÃO CADASTRAR NOVO USUÁRIO
        elif opcao == "nc":
            criar_cliente(clientes)

        # OPERAÇÃO CADASTRAR NOVA CONTA
        elif opcao == "cc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, clientes)

            if conta:
                contas.append(conta)

        # OPERAÇÃO LISTAR CONTAS
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q":
            system('cls')
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            sleep(5)

    print("\nObrigado pela preferência. Tenha um bom dia!\n")


main()
