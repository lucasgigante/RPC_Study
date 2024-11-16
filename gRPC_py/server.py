'''
DSID - EP - Remote Procedure Calls (RPC)

Lucas da Silva Serralheiro Gigante       NUSP: 12691898
Pietro Zalla                             NUSP: 12717606
'''

import math
from concurrent import futures
import logging
from Carro import Carro
import numpy as np

import grpc

import teste_pb2, teste_pb2_grpc


class ServiceServicer(teste_pb2_grpc.ServiceServicer):
    def method1(self, request, context):
        # Method 1: No parameters and no return value
        print("Method 1: retornando void")
        return teste_pb2.Nada()

    def method2(self, request, context):
        # Method 1: No parameters and no return value
        print("Método 2: retornando o dobro de", request.long)
        request.long = request.long * 2
        return teste_pb2.Long(long=request.long)

    def method3(self, request, context):
        # Method 1: No parameters and no return value
        print("Método 3: retornando a soma de", request.listasoma)
        soma = sum(request.listasoma)
        return teste_pb2.Long(long=soma)

    def method4(self, request, context):
        # Method 1: No parameters and no return value
        print("Method 4: retornando n, tal que 2^n >= x, com x sendo o comprimento de:", request.valor)
        result = len(request.valor)
        n = math.ceil(math.log2(result))
        return teste_pb2.String(valor=f"O comprimento da string eh menor que 2 elevado por {n}")

    def method5(self, request, context):
        # Method 1: No parameters and no return value
        carro = Carro(request.marca, request.modelo, request.ano, request.cor)
        print("Method 5: pintando de azul o carro:", carro)
        carro.cor = "Azul"
        return teste_pb2.Carro(marca=carro.marca, modelo=carro.modelo, ano=carro.ano, cor=carro.cor, velocidade=carro.velocidade)

    def method6(self, request, context):
        matrizes = request.matrizes

        if len(matrizes) != 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Exactly two matrices are required.')
            return teste_pb2.MatrizResposta()

        matriz1 = matrizes[0]
        matriz2 = matrizes[1]

        print("Method 6: multiplicando as seguintes matrizes:", matriz1, matriz2)

        if len(matriz1.dimencao) != 2 or len(matriz2.dimencao) != 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Matrices must be two-dimensional.')
            return teste_pb2.MatrizResposta()

        if matriz1.dimencao[1] != matriz2.dimencao[0]:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid matrix dimensions for multiplication.')
            return teste_pb2.MatrizResposta()

        result_dimensions = [matriz1.dimencao[0], matriz2.dimencao[1]]
        result_elements = []

        for i in range(matriz1.dimencao[0]):
            for j in range(matriz1.dimencao[1]):
                element = 0.0
                for k in range(matriz1.dimencao[1]):
                    element += matriz1.elementos[i * matriz1.dimencao[1] + k] * matriz2.elementos[k * matriz2.dimencao[1] + j]
                result_elements.append(element)

        result_matrix = teste_pb2.Matriz()
        result_matrix.dimencao.extend(result_dimensions)
        result_matrix.elementos.extend(result_elements)

        return teste_pb2.MatrizResposta(result=result_matrix)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    teste_pb2_grpc.add_ServiceServicer_to_server(ServiceServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
