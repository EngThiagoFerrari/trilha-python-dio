from abc import ABC, abstractmethod
from datetime import datetime
from os import system
from time import sleep
import textwrap




class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDEPÓSITO REALIZADO COM SUCESSO!\n")
            sleep(3)
        else:
            print("\nFALHA DA OPERAÇÃO! O VALOR INFORMADO É INVÁLIDO.\n")
            sleep(3)
            return False
        
        return True
                
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nFALHA NA OPERAÇÃO! SALDO INSUFICIENTE.\n")
            sleep(3)
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\nSAQUE REALIZADO COM SUCESSO!\n")
            sleep(3)

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nFALHA NA OPERAÇÃO! O VALOR DO SAQUE EXCEDE O VALOR LIMITE POR SAQUE\n")
            sleep(3)

        elif excedeu_saques:
            print("\nFALAHA NA OPERAÇÃO! O NÚMERO DE SAQUES FOI EXCEDIDO.\n")
            sleep(3)

        else:
            return super().sacar(valor)

        return False

    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                #"data": datetime.now().strftime("%d-%m-%Y %H:%M:%s") => bug corrigido - o formato do segundo estava incorreto o que ocasionava erros
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self.transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao


class IteradorContas:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
                Agência:\t{conta.agencia}
                Número:\t\t{conta.numero}
                Titular:\t{conta.cliente.nome}
                Saldo:\t\tR$ {conta.saldo:.2f}
                """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


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


def buscar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nFALHA NA OPERAÇÃO! O CLIENTE NÃO POSSUI CONTA!\n")
        return
    
    # FIXME: Este código não permite a escolha da conta do cliente - retorna a primeiro. Como sugestão de melhoria, esta escolha pode ser implementada
    return cliente.contas[0]


def depositar(clientes):
    system("cls")
    print("\tOperação selecionada => Depositar")
    cpf = input("\nInforme o CPF (somente número): ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\nUsuário não encontrado!\n")
        print("Verifique se o CPF está correto e repita a operação.")
        sleep(3)
        return
    
    valor = float(input("\nInfome o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    system("cls")
    print("\tOperação selecionada => Sacar")
    cpf = input("\nInforme o CPF (somente número): ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\nUsuário não encontrado!\n")
        print("Verifique se o CPF está correto e repita a operação.")
        sleep(3)
        return
    
    valor = float(input("\nInfome o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente => ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!\n")
        sleep(3)
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
        
    system('cls')
    largura_extrato = 50
    extrato = ""

    print(" EXTRATO ".center(largura_extrato, "="))
    tem_transacao = False
    
    for transacao in conta.historico.gerar_relatorio(tipo_transacao=None):#"saque" => resolvido bug no código):
        tem_transacao = True
        trans_data_format = f"\n  {transacao['data']}\t"
        trans_tipo_format = f"{transacao['tipo']}"
        trans_valor_format = f"R$ {transacao['valor']:.2f}".rjust(47 - len(trans_data_format + trans_tipo_format))
        extrato += trans_data_format + trans_tipo_format + trans_valor_format
        #extrato += f"\n  {transacao['tipo']}" + f"R$ {transacao['valor']:.2f}".rjust(48 - len(f"  {transacao['tipo']}")) + f"  {transacao['data']}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"
    
    print(extrato)
    print("-" * largura_extrato)
    print("  Saldo total:".ljust(0) + f"R$ {conta.saldo:.2f}".rjust((48 - len("  Saldo total:"))))
    print("=" * largura_extrato)
    print(input("\nPressione a tecla ENTER para voltar ao menu."))
    

def criar_cliente(clientes):
    system("cls")
    print("\tOperação selecionada => Cadastrar novo Cliente")
    cpf = input("Informe o CPF (somente número): ")
    cliente = buscar_cliente(cpf, clientes)

    if cliente:
        print("\nFALHA NA OPERAÇÃO")
        print("\n\nAtenção! Este CPF já está cadastrado.\n")
        sleep(3)
        return
        
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado):\n=> ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)

    print("\nCLIENTE CRIADO COM SUCESSO!")
    print(input("Pressione a tecla 'ENTER' para voltar ao Menu principal."))


def criar_conta(numero_conta, clientes, contas):
    system("cls")
    print("\tOperação selecionada => Cadastrar novo Conta")
    cpf = input("Informe o CPF (somente número): ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\nUsuário não encontrado, o processo de criação de conta foi encerrado!\n")
        sleep(3)
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!\n")
    sleep(3)


def listar_contas(contas):
    system('cls')
    print("\tExibindo lista de Contas cadastradas:\n")
    print(100 * "=")    
    
    for conta in IteradorContas(contas):
        print("-" * 100)
        print(textwrap.dedent(str(conta)))

    print(input("Pressione a tecla 'ENTER' para voltar o menu."))


def main():
    # LIMITE_SAQUES = 3
    # AGENCIA = "0001"

    # saldo = 0
    # limite = 500
    # extrato = ""
    # numero_saques = 0

    clientes = []
    contas = []
    

    while True:
        # MENU INICIAL
        opcao = menu()

        # OPERAÇÃO DEPÓSITO
        if opcao == "d":
            depositar(clientes)
            
        # OPERAÇÃO SAQUE
        elif opcao == "s":
            sacar(clientes)
            
        # OPERAÇÃO DE EXIBIR EXTRATO    
        elif opcao == "e":
            exibir_extrato(clientes)

        # OPERAÇÃO CADASTRAR NOVO USUÁRIO
        elif opcao == "nc":
            criar_cliente(clientes)

        # OPERAÇÃO CADASTRAR NOVA CONTA
        elif opcao == "cc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

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
