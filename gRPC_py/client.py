'''
DSID - EP - Remote Procedure Calls (RPC)

Lucas da Silva Serralheiro Gigante       NUSP: 12691898
Pietro Zalla                             NUSP: 12717606
'''

import teste_pb2
import teste_pb2_grpc
import grpc
import numpy as np
from Carro import Carro
import time
import random
import string
import matplotlib.pyplot as plt


def get_matrix_dimensions_random(matrix_number):
    rows = random.randint(3, 10)
    columns = rows
    return (rows, columns)


def get_matrix_dimensions(matrix_number):
    print(f"Informe as dimensões das matrizes:")
    rows = int(input("Número de linhas/colunas: "))
    columns = rows
    return (rows, columns)


def get_matrix_elements_random(rows, columns):
    elementos = []
    print("Informe os elementos da matriz:")
    for i in range(rows):
        for j in range(columns):
            element = float(random.randint(1, 150000))
            elementos.append(element)
    return elementos


def get_matrix_elements(rows, columns):
    elementos = []
    print("Informe os elementos da matriz:")
    for i in range(rows):
        for j in range(columns):
            element = float(input(f"Elemento [{i}, {j}]: "))
            elementos.append(element)
    return elementos


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = teste_pb2_grpc.ServiceStub(channel)

        request = teste_pb2.Nada()
        stub.method1(request)

        while True:
            method = input("Qual método você deseja utilizar?\n\n"
                           "\t- Método com 0 argumentos e retorno void (method1),\n"
                           "\t- Método com 1 argumento 'long' e retorno 'long' (method2),\n"
                           "\t- Método com 8 argumentos 'long' e retorno 'long' (method3),\n"
                           "\t- Método com 1 argumento 'str' e retorno 'str' (method4)\n"
                           "\t- Método com 1 argumento 'Carro' e retorno 'Carro' (method5)\n"
                           "\t- Método com 1 argumento 'matriz quadrada (float)' e retorno 'matriz quadrada (float)' (method6)\n"
                           "\t- Teste automatizado de todos os métodos (auto)\n")

            if method == "method1":
                request = teste_pb2.Nada()
                start_time = time.time()
                stub.method1(request)
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                print("Tempo de execução:", execution_time_ms, "milissegundos")
            elif method == "method2":
                arg1 = np.int64(input("Informe o valor a ser dobrado: "))
                request = teste_pb2.Long(long=arg1)
                start_time = time.time()
                response = stub.method2(request)
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                print("Tempo de execução:", execution_time_ms, "milissegundos")
                print(response)
            elif method == "method3":
                args = []
                for i in range(1, 9):
                    arg = np.int64(input(f"Informe o valor {i}/8: "))
                    args.append(arg)
                request = teste_pb2.LongList(listasoma=args)
                start_time = time.time()
                response = stub.method3(request)
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                print("Tempo de execução:", execution_time_ms, "milissegundos")
                print(response)
            elif method == "method4":
                arg1 = input("Informe o valor para arg1: ")
                request = teste_pb2.String(valor=arg1)
                start_time = time.time()
                response = stub.method4(request)
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                print("Tempo de execução:", execution_time_ms, "milissegundos")
                print(response)
            elif method == "method5":
                marca = input("Informe a marca do carro: ")
                modelo = input("Informe o modelo do carro: ")
                ano = int(input("Informe o ano do carro: "))
                cor = input("Informe a cor do carro: ")
                carro = Carro(marca, modelo, ano, cor)

                print("\n\nCarro antigo:\n\t", carro)
                request = teste_pb2.Carro(marca=carro.marca, modelo=carro.modelo, ano=carro.ano, cor=carro.cor,
                                          velocidade=carro.velocidade)

                start_time = time.time()
                response = stub.method5(request)
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                print("Tempo de execução:", execution_time_ms, "milissegundos")

                carro = Carro(response.marca, response.modelo, response.ano, response.cor)
                print("\nCarro novo:\n\t", carro)
                print("\n")
            elif method == "method6":

                request = teste_pb2.MatrizesRequest()

                # Matriz 1
                matrix1_rows, matrix1_columns = get_matrix_dimensions(1)
                print("MATRIZ 1:")
                matrix1_elements = get_matrix_elements(matrix1_rows, matrix1_columns)

                matriz1 = teste_pb2.Matriz()
                matriz1.dimencao.extend([matrix1_rows, matrix1_columns])
                matriz1.elementos.extend(matrix1_elements)
                request.matrizes.append(matriz1)

                # Matriz 2
                matrix2_rows = matrix1_rows
                matrix2_columns = matrix1_columns
                print("MATRIZ 2:")
                matrix2_elements = get_matrix_elements(matrix2_rows, matrix2_columns)

                matriz2 = teste_pb2.Matriz()
                matriz2.dimencao.extend([matrix2_rows, matrix2_columns])
                matriz2.elementos.extend(matrix2_elements)
                request.matrizes.append(matriz2)

                start_time = time.time()
                response = stub.method6(request)
                end_time = time.time()
                execution_time_ms = (end_time - start_time) * 1000
                print("Tempo de execução:", execution_time_ms, "milissegundos")
                # Exibe o resultado da multiplicação das matrizes
                result_matrix = response.result
                print("Resultado:")
                for i in range(result_matrix.dimencao[0]):
                    row_elements = result_matrix.elementos[
                                   i * result_matrix.dimencao[1]: (i + 1) * result_matrix.dimencao[1]]
                    print(row_elements)

            elif method == "auto":

                nVezes = int(input("Quantas vezes você deseja que cada método seja executado?"))

                tempo1 = []
                tempo2 = []
                tempo3 = []
                tempo4 = []
                tempo5 = []
                tempo6 = []

                request = teste_pb2.Nada()
                stub.method1(request)
                for i in range(nVezes):
                    request = teste_pb2.Nada()
                    start_time = time.time()
                    stub.method1(request)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # Tempo de execução em milissegundos
                    print(f"Resposta {i + 1}: nada")
                    print(f"Tempo de execução do método method1: {execution_time} ms\n\n")
                    tempo1.append(execution_time)
                for i in range(nVezes):
                    arg1 = np.int64(i * i)
                    request = teste_pb2.Long(long=arg1)
                    start_time = time.time()
                    response = stub.method2(request)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # Tempo de execução em milissegundos
                    print(f"Resposta {i + 1}:", response)
                    print(f"Tempo de execução do método method2: {execution_time} ms")
                    tempo2.append(execution_time)
                for i in range(nVezes):
                    args = np.random.randint(1, 1000000, size=8).tolist()
                    start_time = time.time()
                    response = stub.method3(request)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # Tempo de execução em milissegundos
                    print(f"Resposta {i + 1}:", response)
                    print(f"Tempo de execução do método method3: {execution_time} ms")
                    tempo3.append(execution_time)
                for i in range(nVezes):
                    length = random.randint(1, 7500)
                    arg1 = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
                    request = teste_pb2.String(valor=arg1)
                    start_time = time.time()
                    response = stub.method4(request)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # Tempo de execução em milissegundos
                    print(f"Resposta {i + 1}:", response)
                    print(f"Tempo de execução do método method4: {execution_time} ms")
                    tempo4.append(execution_time)
                for i in range(nVezes):
                    marca = np.random.choice(["Ferrari", "Ford", "Chevrolet", "BMW"])
                    modelo = np.random.choice(["Uno", "Fiesta", "Camaro", "X5"])
                    ano = np.random.randint(2000, 2023)
                    cor = np.random.choice(["Vermelho", "Branco", "Prata", "Preto"])
                    carro = Carro(marca, modelo, ano, cor)
                    request = teste_pb2.Carro(marca=carro.marca, modelo=carro.modelo, ano=carro.ano, cor=carro.cor,
                                              velocidade=carro.velocidade)
                    start_time = time.time()
                    response = stub.method5(request)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # Tempo de execução em milissegundos
                    carro = Carro(response.marca, response.modelo, response.ano, response.cor)
                    print(f"Resposta {i + 1}:", carro)
                    print(f"Tempo de execução do método method5: {execution_time} ms")
                    tempo5.append(execution_time)
                for i in range(nVezes):
                    request = teste_pb2.MatrizesRequest()

                    # Matriz 1
                    matrix1_rows, matrix1_columns = get_matrix_dimensions_random(1)
                    print("MATRIZ 1:")
                    matrix1_elements = get_matrix_elements_random(matrix1_rows, matrix1_columns)

                    matriz1 = teste_pb2.Matriz()
                    matriz1.dimencao.extend([matrix1_rows, matrix1_columns])
                    matriz1.elementos.extend(matrix1_elements)
                    request.matrizes.append(matriz1)

                    # Matriz 2
                    matrix2_rows = matrix1_rows
                    matrix2_columns = matrix1_columns
                    print("MATRIZ 2:")
                    matrix2_elements = get_matrix_elements_random(matrix2_rows, matrix2_columns)

                    matriz2 = teste_pb2.Matriz()
                    matriz2.dimencao.extend([matrix2_rows, matrix2_columns])
                    matriz2.elementos.extend(matrix2_elements)
                    request.matrizes.append(matriz2)

                    start_time = time.time()
                    response = stub.method6(request)
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000
                    print(f"Tempo de execução do método method5: {execution_time} ms")
                    tempo6.append(execution_time)

                media1 = np.mean(tempo1)
                media2 = np.mean(tempo2)
                media3 = np.mean(tempo3)
                media4 = np.mean(tempo4)
                media5 = np.mean(tempo5)
                media6 = np.mean(tempo6)
                tempo_medio = [media1, media2, media3, media4, media5, media6]
                tempos_execucao = [tempo1, tempo2, tempo3, tempo4, tempo5, tempo6]

                desvio1 = np.std(tempo1)
                desvio2 = np.std(tempo2)
                desvio3 = np.std(tempo3)
                desvio4 = np.std(tempo4)
                desvio5 = np.std(tempo5)
                desvio6 = np.std(tempo6)
                desvio_padrao = [desvio1, desvio2, desvio3, desvio4, desvio5, desvio6]

                # Metodo1
                experimentos = []
                for i in range(nVezes):
                    valor = f"Ex. {i + 1}"
                    experimentos.append(valor)

                plt.plot(range(len(experimentos)), tempo1, label='Dados')  # Linha dos dados
                plt.axhline(media1, color='red', linestyle='--', label='Média')  # Linha da média
                plt.axhline(media1 + desvio1, color='green', linestyle='--',
                            label='Média + Desvio Padrão')  # Linha da média + desvio padrão
                plt.axhline(media1 - desvio1, color='green', linestyle='--',
                            label='Média - Desvio Padrão')  # Linha da média - desvio padrão

                plt.xticks(range(len(experimentos)), experimentos)
                plt.xlabel('Execução')
                plt.ylabel('Tempo de Execução (ms)')
                plt.title('Método 1')
                plt.tight_layout()
                plt.legend()

                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media1, f'{media1:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico do desvio padrão
                plt.text(len(experimentos) - 1, media1 + desvio1, f'{desvio1:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media1 - desvio1, f'-{desvio1:.2f}', ha='right', va='bottom')

                plt.show()


                # Metodo2
                experimentos = []
                for i in range(nVezes):
                    valor = f"Ex. {i + 1}"
                    experimentos.append(valor)

                plt.plot(range(len(experimentos)), tempo2, label='Dados')  # Linha dos dados
                plt.axhline(media2, color='red', linestyle='--', label='Média')  # Linha da média
                plt.axhline(media2 + desvio2, color='green', linestyle='--',
                            label='Média + Desvio Padrão')  # Linha da média + desvio padrão
                plt.axhline(media2 - desvio2, color='green', linestyle='--',
                            label='Média - Desvio Padrão')  # Linha da média - desvio padrão

                plt.xticks(range(len(experimentos)), experimentos)
                plt.xlabel('Execução')
                plt.ylabel('Tempo de Execução (ms)')
                plt.title('Método 2')
                plt.tight_layout()
                plt.legend()

                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media2, f'{media2:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico do desvio padrão
                plt.text(len(experimentos) - 1, media2 + desvio2, f'{desvio2:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media2 - desvio2, f'-{desvio2:.2f}', ha='right', va='bottom')

                plt.show()

                # Metodo3
                experimentos = []
                for i in range(nVezes):
                    valor = f"Ex. {i + 1}"
                    experimentos.append(valor)

                plt.plot(range(len(experimentos)), tempo3, label='Dados')  # Linha dos dados
                plt.axhline(media3, color='red', linestyle='--', label='Média')  # Linha da média
                plt.axhline(media3 + desvio3, color='green', linestyle='--',
                            label='Média + Desvio Padrão')  # Linha da média + desvio padrão
                plt.axhline(media3 - desvio3, color='green', linestyle='--',
                            label='Média - Desvio Padrão')  # Linha da média - desvio padrão

                plt.xticks(range(len(experimentos)), experimentos)
                plt.xlabel('Execução')
                plt.ylabel('Tempo de Execução (ms)')
                plt.title('Método 3')
                plt.tight_layout()
                plt.legend()

                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media3, f'{media3:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico do desvio padrão
                plt.text(len(experimentos) - 1, media3 + desvio3, f'{desvio3:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media3 - desvio3, f'-{desvio3:.2f}', ha='right', va='bottom')

                plt.show()

                # Metodo4
                experimentos = []
                for i in range(nVezes):
                    valor = f"Ex. {i + 1}"
                    experimentos.append(valor)

                plt.plot(range(len(experimentos)), tempo4, label='Dados')  # Linha dos dados
                plt.axhline(media4, color='red', linestyle='--', label='Média')  # Linha da média
                plt.axhline(media4 + desvio4, color='green', linestyle='--',
                            label='Média + Desvio Padrão')  # Linha da média + desvio padrão
                plt.axhline(media4 - desvio4, color='green', linestyle='--',
                            label='Média - Desvio Padrão')  # Linha da média - desvio padrão

                plt.xticks(range(len(experimentos)), experimentos)
                plt.xlabel('Execução')
                plt.ylabel('Tempo de Execução (ms)')
                plt.title('Método 4')
                plt.tight_layout()
                plt.legend()

                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media4, f'{media4:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico do desvio padrão
                plt.text(len(experimentos) - 1, media4 + desvio4, f'{desvio4:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media4 - desvio4, f'-{desvio4:.2f}', ha='right', va='bottom')

                plt.show()

                # Metodo5
                experimentos = []
                for i in range(nVezes):
                    valor = f"Ex. {i + 1}"
                    experimentos.append(valor)

                plt.plot(range(len(experimentos)), tempo5, label='Dados')  # Linha dos dados
                plt.axhline(media5, color='red', linestyle='--', label='Média')  # Linha da média
                plt.axhline(media5 + desvio5, color='green', linestyle='--',
                            label='Média + Desvio Padrão')  # Linha da média + desvio padrão
                plt.axhline(media5 - desvio5, color='green', linestyle='--',
                            label='Média - Desvio Padrão')  # Linha da média - desvio padrão

                plt.xticks(range(len(experimentos)), experimentos)
                plt.xlabel('Execução')
                plt.ylabel('Tempo de Execução (ms)')
                plt.title('Método 5')
                plt.tight_layout()
                plt.legend()

                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media5, f'{media5:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico do desvio padrão
                plt.text(len(experimentos) - 1, media5 + desvio5, f'{desvio5:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media5 - desvio5, f'-{desvio5:.2f}', ha='right', va='bottom')

                plt.show()

                # Metodo6
                experimentos = []
                for i in range(nVezes):
                    valor = f"Ex. {i + 1}"
                    experimentos.append(valor)

                plt.plot(range(len(experimentos)), tempo6, label='Dados')  # Linha dos dados
                plt.axhline(media6, color='red', linestyle='--', label='Média')  # Linha da média
                plt.axhline(media6 + desvio6, color='green', linestyle='--',
                            label='Média + Desvio Padrão')  # Linha da média + desvio padrão
                plt.axhline(media6 - desvio6, color='green', linestyle='--',
                            label='Média - Desvio Padrão')  # Linha da média - desvio padrão

                plt.xticks(range(len(experimentos)), experimentos)
                plt.xlabel('Execução')
                plt.ylabel('Tempo de Execução (ms)')
                plt.title('Método 6')
                plt.tight_layout()
                plt.legend()

                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media6, f'{media6:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico do desvio padrão
                plt.text(len(experimentos) - 1, media6 + desvio6, f'{desvio6:.2f}', ha='right', va='bottom')
                # Adiciona o valor numérico da média
                plt.text(len(experimentos) - 1, media6 - desvio6, f'-{desvio6:.2f}', ha='right', va='bottom')

                plt.show()

                teste = input("Deseja imprimir outros gráficos? (sim/nao)\n")
                if teste.lower() == "sim":

                    metodos = ['Method 1', 'Method 2', 'Method 3', 'Method 4', 'Method 5', 'Method6']
                    x_pos = np.arange(len(metodos))

                    plt.bar(x_pos, tempo_medio, yerr=desvio_padrao, align='center', alpha=0.5)
                    plt.xticks(x_pos, metodos)
                    plt.ylabel('Tempo de Execução (ms)')
                    plt.title('Tempo Médio de Execução e Desvio Padrão por Método')

                    # Adiciona o valor numérico em cada barra
                    for i, j in enumerate(tempo_medio):
                        plt.text(i, j, f'{j:.2f}', ha='center', va='bottom', color='red')

                    # Adiciona o valor do desvio padrão em cada coluna
                    for i, (j, err) in enumerate(zip(tempo_medio, desvio_padrao)):
                        plt.text(i, j + err, f'{err:.2f}', ha='center', va='bottom', color='green')

                    plt.show()

                    for i in range(len(metodos)):
                        plt.plot(range(1, len(tempos_execucao[i]) + 1), tempos_execucao[i], label=metodos[i])

                    plt.xlabel('Execução')
                    plt.ylabel('Tempo de Execução (ms)')
                    plt.title('Tempo de Execução por Método')
                    plt.legend()
                    plt.show()

                    plt.boxplot(tempos_execucao, labels=metodos)

                    plt.xlabel('Método')
                    plt.ylabel('Tempo de Execução (ms)')
                    plt.title('Distribuição do Tempo de Execução por Método')
                    plt.show()

                    for i in range(len(metodos)):
                        plt.scatter(range(1, len(tempos_execucao[i]) + 1), tempos_execucao[i], label=metodos[i])

                    plt.xlabel('Execução')
                    plt.ylabel('Tempo de Execução (ms)')
                    plt.title('Tempo de Execução por Método')
                    plt.legend()
                    plt.show()

            teste = input("Deseja continuar? (sim/nao)\n")
            if teste.lower() != "sim":
                break


if __name__ == "__main__":
    run()
