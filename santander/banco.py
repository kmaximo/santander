class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = "0001"
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0.0
        self.limite = 500.0
        self.extrato = []
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.contador_contas = 1

    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        """Cadastra um novo usuário (cliente)"""
        if self._buscar_usuario_por_cpf(cpf):
            return False, "Já existe um usuário com este CPF!"
        
        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)
        return True, "Usuário cadastrado com sucesso!"

    def cadastrar_conta(self, cpf_usuario):
        """Cadastra uma nova conta para um usuário existente"""
        usuario = self._buscar_usuario_por_cpf(cpf_usuario)
        if not usuario:
            return False, "Usuário não encontrado!"
        
        numero_conta = self.contador_contas
        nova_conta = Conta("0001", numero_conta, usuario)
        self.contas.append(nova_conta)
        self.contador_contas += 1
        return True, nova_conta

    def _buscar_usuario_por_cpf(self, cpf):
        """Busca usuário pelo CPF"""
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def buscar_conta_por_numero(self, numero_conta):
        """Busca conta pelo número"""
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                return conta
        return None
        
    def listar_contas(self):
        """Lista todas as contas cadastradas no sistema
        
        Returns:
            list: Lista de dicionários com informações das contas
        """
        contas_formatadas = []
        for conta in self.contas:
            contas_formatadas.append({
                'agencia': conta.agencia,
                'numero_conta': conta.numero_conta,
                'titular': conta.usuario.nome,
                'cpf_titular': conta.usuario.cpf,
                'saldo': f"R$ {conta.saldo:.2f}"
            })
        return contas_formatadas

    def depositar(self, numero_conta, valor, /):
        """Realiza um depósito na conta"""
        conta = self.buscar_conta_por_numero(numero_conta)
        if not conta:
            return False, "Conta não encontrada!"
        
        if valor > 0:
            conta.saldo += valor
            conta.extrato.append(f"Depósito: R$ {valor:.2f}")
            return True, f"Depósito de R$ {valor:.2f} realizado com sucesso!"
        return False, "Operação falhou! O valor informado é inválido."

    def sacar(self, *, numero_conta, valor):
        """
        Realiza um saque da conta
        
        Args:
            numero_conta (int): Número da conta (keyword-only)
            valor (float): Valor a ser sacado (keyword-only)
            
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        conta = self.buscar_conta_por_numero(numero_conta)
        if not conta:
            return False, "Conta não encontrada!"
        
        excedeu_saldo = valor > conta.saldo
        excedeu_limite = valor > conta.limite
        excedeu_saques = conta.numero_saques >= conta.LIMITE_SAQUES

        if excedeu_saldo:
            return False, "Operação falhou! Você não tem saldo suficiente."
        elif excedeu_limite:
            return False, f"Operação falhou! O valor do saque excede o limite de R$ {conta.limite:.2f}."
        elif excedeu_saques:
            return False, f"Operação falhou! Número máximo de {conta.LIMITE_SAQUES} saques diários excedido."
        elif valor > 0:
            conta.saldo -= valor
            conta.extrato.append(f"Saque: R$ {valor:.2f}")
            conta.numero_saques += 1
            return True, f"Saque de R$ {valor:.2f} realizado com sucesso!"
        else:
            return False, "Operação falhou! O valor informado é inválido."

    def gerar_extrato(self, numero_conta, /, *, detalhado=False):
        """
        Gera o extrato da conta
        
        Args:
            numero_conta (int): Número da conta (positional-only)
            detalhado (bool): Se True, mostra informações adicionais (keyword-only)
            
        Returns:
            tuple: (extrato: list, saldo: float, erro: str or None)
        """
        conta = self.buscar_conta_por_numero(numero_conta)
        if not conta:
            return None, None, "Conta não encontrada!"
        
        extrato = conta.extrato.copy()
        
        if detalhado:
            extrato.insert(0, f"Agência: {conta.agencia}")
            extrato.insert(1, f"Conta: {conta.numero_conta}")
            extrato.insert(2, f"Titular: {conta.usuario.nome}")
            extrato.insert(3, "=" * 40)
        
        return extrato, conta.saldo, None

    def obter_status(self, numero_conta):
        """Retorna o status atual da conta"""
        conta = self.buscar_conta_por_numero(numero_conta)
        if not conta:
            return None, "Conta não encontrada!"
        
        return {
            'agencia': conta.agencia,
            'numero_conta': conta.numero_conta,
            'usuario': conta.usuario.nome,
            'saldo': conta.saldo,
            'saques_restantes': conta.LIMITE_SAQUES - conta.numero_saques,
            'limite_saque': conta.limite
        }, None