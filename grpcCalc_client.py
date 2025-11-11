import grpc
import grpcCalc_pb2
import grpcCalc_pb2_grpc
import pybreaker
import time
import os

# Configuração do Circuit Breaker (protege contra falhas repetidas)
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=5)

@breaker
def connect():
    channel = grpc.insecure_channel('localhost:8080')
    client = grpcCalc_pb2_grpc.apiStub(channel)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== CALCULADORA RPC ===")
        print("1. Adição")
        print("2. Subtração")
        print("3. Multiplicação")
        print("4. Divisão")
        print("0. Sair")
        print("========================")

        opcao = input("Escolha a operação: ")

        if opcao == "0":
            print("Saindo da calculadora...")
            break

        if opcao not in ["1", "2", "3", "4"]:
            print("⚠️ Opção inválida. Tente novamente.")
            time.sleep(2)
            continue

        try:
            x = float(input("Entre com o primeiro número: "))
            y = float(input("Entre com o segundo número: "))

            if opcao == "1":
                res = client.add(grpcCalc_pb2.args(numOne=x, numTwo=y))
                print(f"Resultado da soma: {res.num}")

            elif opcao == "2":
                res = client.sub(grpcCalc_pb2.args(numOne=x, numTwo=y))
                print(f"Resultado da subtração: {res.num}")

            elif opcao == "3":
                res = client.mul(grpcCalc_pb2.args(numOne=x, numTwo=y))
                print(f"Resultado da multiplicação: {res.num}")

            elif opcao == "4":
                if y == 0:
                    print("❌ Erro: divisão por zero não permitida.")
                else:
                    res = client.div(grpcCalc_pb2.args(numOne=x, numTwo=y))
                    print(f"Resultado da divisão: {res.num}")

        except ValueError:
            print("⚠️ Entrada inválida! Digite apenas números.")
        except grpc.RpcError as e:
            print(f"Erro de comunicação com o servidor: {e}")
        except pybreaker.CircuitBreakerError:
            print("🚫 Circuit Breaker ativado: servidor indisponível.")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    connect()
