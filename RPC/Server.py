'''
DSID - EP - Remote Procedure Calls (RPC)

Lucas da Silva Serralheiro Gigante       NUSP: 12691898
Pietro Zalla                             NUSP: 12717606
'''

import json
import math
import jsonpickle
from Carro import Carro
from jsonrpcserver import Success, method, serve, InvalidParams, Result, Error
import re
import numpy as np


@method
def method1() -> Result:
    # Method 1: No parameters and no return value
    print("Method 1: retornando void")
    return Success()


@method
def method2(arg1: str) -> Result:
    # Método 2: Aceita um único argumento do tipo int64 e retorna o dobro do valor
    arg1 = jsonpickle.decode(arg1)
    print("Método 2: retornando o dobro de", arg1)
    return Success(jsonpickle.encode(arg1 * np.int64(2)))


@method
def method3(args: str) -> Result:
    args = jsonpickle.decode(args)
    print("Método 3: somando os valores:")
    for arg in args:
        print(arg, "\n")
    print("\n")

    # Método 3: Aceita uma lista de 8 argumentos do tipo int64 e retorna a soma deles
    if len(args) != 8:
        return Error("A lista deve conter exatamente 8 valores")
    try:
        result = np.sum(args, dtype=np.int64)
        return Success(jsonpickle.encode(result))
    except ValueError:
        return Error("Argumento inválido: Todos os argumentos devem ser inteiros")


@method
def method4(arg1: str) -> Result:
    # Method 4: Accepts a string argument and returns its length
    arg1 = jsonpickle.decode(arg1)

    print("Method 4: retornando n, tal que 2^n >= x, com x sendo o comprimento de:", arg1)
    try:
        result = len(arg1)
        n = math.ceil(math.log2(result))
        return Success(jsonpickle.encode(f"O comprimento da string eh menor que 2 elevado por {n}"))
    except Exception as e:
        return Error(str(e))


@method
def method5(arg1: str) -> Result:
    # Method 4: Accepts a string argument and returns its length
    arg = jsonpickle.decode(arg1)
    print("Method 5: pintando de azul o carro:", arg)
    arg.cor = "Azul"
    arg2 = jsonpickle.encode(arg)
    return Success(arg2)


@method
def method6(arg1: str, arg2: str) -> Result:
    mat1 = jsonpickle.decode(arg1)
    mat2 = jsonpickle.decode(arg2)

    matriz1 = mat1
    matriz2 = mat2

    # Verifica se as matrizes têm as mesmas dimensões
    if len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0]):
        raise ValueError("As matrizes devem ter as mesmas dimensões.")

    # Inicializa a matriz de resultado com zeros
    result_matriz = [[0] * len(matriz1[0]) for _ in range(len(matriz1))]

    # Multiplica as matrizes
    for i in range(len(matriz1)):
        for j in range(len(matriz2[0])):
            for k in range(len(matriz2)):
                result_matriz[i][j] += matriz1[i][k] * matriz2[k][j]

    arg2 = jsonpickle.encode(result_matriz)

    return Success(arg2)


if __name__ == "__main__":
    serve("localhost", 8545)
