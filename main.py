import abc
from abc import ABC, abstractmethod
from datetime import datetime

LIMITE_POR_SAQUE = 500
LIMITE_SAQUES = 3


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco

        self.contas: list = []
        self.conta_atual: Conta | None = None

    @staticmethod
    def realizar_transacao(conta, transacao):
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, dt_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.dt_nascimento = dt_nascimento
        super().__init__(endereco)


class Transacao(ABC):
    @property
    @abc.abstractmethod
    def valor(self):
        pass

    @property
    @abc.abstractmethod
    def tipo(self):
        pass

    @property
    @abc.abstractmethod
    def data(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
        self._tipo = "-"
        self._data = datetime.now()

    def registrar(self, conta):
        ret, msg = conta.sacar(self.valor)
        if ret:
            conta.historico.adicionar_transacao(self)

        return msg

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, value):
        self._valor = value

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
        self._tipo = "+"
        self._data = datetime.now()

    def registrar(self, conta):
        ret, msg = conta.depositar(self.valor)
        if ret:
            conta.historico.adicionar_transacao(self)

        return msg

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, value):
        self._valor = value

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class Historico:
    def __init__(self):
        self._transacoes: list[Transacao] = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(transacao)


class Conta:
    ultima_conta = 0
    limite = LIMITE_POR_SAQUE

    def __init__(self, agencia: str, cliente: Cliente):
        self.numero_saques: int = 0
        self._saldo: float = 0.0
        Conta.ultima_conta += 1
        self._numero: int = Conta.ultima_conta
        self._agencia: str = agencia
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

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

    @classmethod
    def nova_conta(cls, cliente: Cliente, agencia):
        cls.ultima_conta += 1

        return cls(agencia, cliente)

    def sacar(self, valor: float):
        if valor > self.saldo:
            msg = "Você não tem saldo suficiente para fazer esse saque. Por favor, verifique se você tem saldo."
            ret = False
        elif valor > 0:
            self.saldo -= valor

            self.numero_saques += 1
            msg = f"Saque realizado com sucesso. Saldo: R$ {self.saldo:.2f}"
            ret = True
        else:
            msg = "Por favor, informe um valor maior que 0."
            ret = False
        return ret, msg

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            msg = f"Depósito realizado com sucesso. Saldo: R$ {self.saldo:.2f}"
            ret = True
        else:
            msg = "Por favor, informe um valor maior que 0."
            ret = False
        return ret, msg

    def mostra_extrato(self):
        saida = "EXTRATO DE CONTA:"
        for transacao in self.historico.transacoes:
            msg = f"{transacao.tipo} {transacao.valor}"
            # print(msg)
            saida += msg

        msg = f"\nSaldo: R$ {self.saldo}"
        saida += msg
        # print(msg)
        return saida


class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques, agencia: str, cliente: Cliente):
        self.limite = limite
        self.limite_saques = limite_saques
        super().__init__(agencia, cliente)

    def sacar(self, valor: float):
        if valor > self.limite:
            msg = ("Não foi possível fazer o saque pois o valor excede o limite da transação. Por favor, "
                   "escolha outro valor.")
            ret = False

        elif self.numero_saques >= self.limite_saques:
            msg = "Você excedeu a quantidade diária de saques permitida. Por favor, tente novamente amanhã."
            ret = False
        else:
            ret, msg = super().sacar(valor)

        return ret, msg


def listar_usuarios(lista_usuarios):
    saida = "LISTA DE USUÁRIOS DO BANCO\n"
    for cpf, cliente in lista_usuarios.items():
        saida += f"{cpf}: {cliente.nome}\n"

    return saida


def listar_contas(lista_usuarios):
    saida = "LISTA DE CONTAS DO BANCO\n"

    for cpf, cliente in lista_usuarios.items():
        for cta in cliente.contas:
            saida += f"{cta.numero}: {cpf} ({cliente.nome})\n"

    return saida


def form_usuario():
    nome = input("Nome: ")
    dt_nascimento = input("Data de Nascimento: ")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    uf = input("Sigla do Estado: ")

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
    return nome, dt_nascimento, endereco


def novo_usuario():
    print("Criando novo usuário")
    print("--------------------")
    cpf = input("CPF: ")
    cpf = cpf.replace(".", "").replace("-", "")

    nome, dt_nascimento, endereco = form_usuario()

    novo_cliente = PessoaFisica(cpf, nome, dt_nascimento, endereco)
    usuarios[cpf] = novo_cliente

    agencia = input("Agência: ")
    cta = ContaCorrente(LIMITE_POR_SAQUE, LIMITE_SAQUES, agencia, novo_cliente)
    novo_cliente.adicionar_conta(cta)

    novo_cliente.conta_atual = cta

    return cpf


def monta_menu(lista_usuarios, usu_atual, msg):
    conta = lista_usuarios[usu_atual].conta_atual
    mnu = f"""
========================================
Você está no banco XYZ
Cliente: {usu_atual}  Conta: {conta.numero}  Agência: {conta.agencia}

[d]  Depositar          [u]  Criar usuário
[s]  Sacar              [c]  Criar conta
[e]  Extrato            [lu] Listar usuários
[q]  Sair               [lc] Lista contas
-----------------
{msg}
=> """

    return mnu


mensagem = ""
usuario_atual: str = ""
usuarios: dict = {}

print("=" * 80)
print("SISTEMA BANCÁRIO - VERSÃO POO".center(80))
print("=" * 80)

while True:
    if not usuario_atual:
        print("Usuario não identificado. Cadastrando um novo cliente.")
        print("------------------------------------------------------")
        usuario_atual = novo_usuario()
    else:
        cta_atual = usuarios[usuario_atual].conta_atual

        menu = monta_menu(usuarios, usuario_atual, mensagem)
        opcao = input(menu)

        mensagem = ""
        if opcao == "d":
            vlr = float(input("Valor do depósito: "))
            trans = Deposito(vlr)
            mensagem = Cliente.realizar_transacao(cta_atual, trans)
        elif opcao == "s":
            vlr = float(input("Valor do depósito: "))
            trans = Saque(vlr)
            mensagem = Cliente.realizar_transacao(cta_atual, trans)

        elif opcao == "e":
            mensagem = usuarios[usuario_atual].conta_atual.mostra_extrato()

        elif opcao == "u":
            usuario_atual = novo_usuario()

        elif opcao == "c":
            print("Criando nova conta")
            print("------------------")
            ag = input("Agência: ")
            nova_conta = ContaCorrente(LIMITE_POR_SAQUE, LIMITE_SAQUES, ag, usuarios[usuario_atual])
            usuarios[usuario_atual].adicionar_conta(nova_conta)
            usuarios[usuario_atual].conta_atual = nova_conta

        elif opcao == "lu":
            mensagem = listar_usuarios(usuarios)

        elif opcao == "lc":
            mensagem = listar_contas(usuarios)

        elif opcao == "q":
            break
        else:
            mensagem = "Operação não reconhecida. Por favor selecione uma das opções acima."
