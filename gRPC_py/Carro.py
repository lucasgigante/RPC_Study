'''
DSID - EP - Remote Procedure Calls (RPC)

Lucas da Silva Serralheiro Gigante       NUSP: 12691898
Pietro Zalla                             NUSP: 12717606
'''

class Carro:
    def __init__(self, marca, modelo, ano, cor):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.velocidade = 0

    def acelerar(self, quantidade):
        self.velocidade += quantidade

    def frear(self, quantidade):
        if quantidade > self.velocidade:
            self.velocidade = 0
        else:
            self.velocidade -= quantidade

    def __str__(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Ano: {self.ano}, Cor: {self.cor}"
