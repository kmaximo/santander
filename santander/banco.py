class Banco:
    def __init__(self):
        self.saldo = 0.0
        self.limite = 500.0
        self.extrato = []
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        """Realiza um depósito na conta"""
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: R$ {valor:.2f}")
            return True, f"Depósito de R$ {valor:.2f} realizado com sucesso!"
        return False, "Operação falhou! O valor informado é inválido."

    def sacar(self, valor):
        """Realiza um saque da conta"""
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            return False, "Operação falhou! Você não tem saldo suficiente."
        elif excedeu_limite:
            return False, f"Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}."
        elif excedeu_saques:
            return False, f"Operação falhou! Número máximo de {self.LIMITE_SAQUES} saques diários excedido."
        elif valor > 0:
            self.saldo -= valor
            self.extrato.append(f"Saque: R$ {valor:.2f}")
            self.numero_saques += 1
            return True, f"Saque de R$ {valor:.2f} realizado com sucesso!"
        else:
            return False, "Operação falhou! O valor informado é inválido."

    def gerar_extrato(self):
        """Retorna o extrato da conta"""
        return self.extrato.copy(), self.saldo

    def obter_status(self):
        """Retorna o status atual da conta"""
        return {
            'saldo': self.saldo,
            'saques_restantes': self.LIMITE_SAQUES - self.numero_saques,
            'limite_saque': self.limite
        }