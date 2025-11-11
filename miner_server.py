import time
import threading
import hashlib
import random

import grpc
from concurrent import futures

import miner_pb2
import miner_pb2_grpc

# -----------------------
# Configurações / Tabela
# -----------------------
# Tabela em memória: lista de dicts com TransactionID, Challenge, Solution, Winner
table_lock = threading.Lock()
table = []

def new_transaction(transaction_id):
    # gera desafio aleatório 1..20 (1 mais fácil)
    challenge = random.randint(1, 20)
    entry = {
        "TransactionID": transaction_id,
        "Challenge": challenge,
        "Solution": "",   # string vazia até alguém achar
        "Winner": -1,
        "Timestamp": int(time.time() * 1000)
    }
    return entry

# inicializa TransactionID = 0 no servidor startup
with table_lock:
    table.append(new_transaction(0))

# -----------------------
# Helper: valida hash SHA-1
# -----------------------
def meets_challenge(candidate: str, challenge: int) -> bool:
    """
    Checa se sha1(candidate).hexdigest() começa com '0' * challenge.
    challenge é 1..20 (número de hex zeros).
    Observação: hex digit = 4 bits. Ajuste conforme necessidade.
    """
    h = hashlib.sha1(candidate.encode('utf-8')).hexdigest()
    return h.startswith('0' * challenge)

# -----------------------
# Implementação do serviço gRPC
# -----------------------
class MinerServicer(miner_pb2_grpc.MinerServicer):
    def GetCurrentChallenge(self, request, context):
        with table_lock:
            current = table[-1]
            return miner_pb2.ChallengeInfo(
                transaction_id=current["TransactionID"],
                challenge=current["Challenge"],
                timestamp=current["Timestamp"]
            )

    def SubmitSolution(self, request, context):
        with table_lock:
            # verifica se a submissão é para o Transaction atual
            current = table[-1]
            if request.transaction_id != current["TransactionID"]:
                return miner_pb2.SubmitResponse(
                    accepted=False,
                    message=f"TransactionID incorreto. Atualmente: {current['TransactionID']}",
                    winner_client_id=current["Winner"] if current["Winner"] is not None else -1,
                    solution=current["Solution"]
                )

            if current["Winner"] != -1:
                return miner_pb2.SubmitResponse(
                    accepted=False,
                    message="Desafio já solucionado.",
                    winner_client_id=current["Winner"],
                    solution=current["Solution"]
                )

            # valida candidato
            ok = meets_challenge(request.candidate, current["Challenge"])
            if ok:
                # registra solução e vencedor
                current["Solution"] = request.candidate
                # client_id vem como string; tentamos converter pra int, se não, deixamos -1 ou hash
                try:
                    winner_id = int(request.client_id)
                except:
                    # se não for int, pode guardar -1 e retornar string no message
                    winner_id = -1
                current["Winner"] = winner_id

                # cria próximo transaction automaticamente (incrementa)
                next_id = current["TransactionID"] + 1
                table.append(new_transaction(next_id))

                return miner_pb2.SubmitResponse(
                    accepted=True,
                    message=f"Solução aceita! Você é o vencedor da tx {current['TransactionID']}.",
                    winner_client_id=current["Winner"],
                    solution=current["Solution"]
                )
            else:
                return miner_pb2.SubmitResponse(
                    accepted=False,
                    message="Solução inválida (hash SHA-1 não atende ao desafio).",
                    winner_client_id=-1,
                    solution=""
                )

    # Método de exemplo (reutiliza seu adder)
    def Add(self, request, context):
        s = request.a + request.b
        return miner_pb2.AdderResponse(sum=s)

# -----------------------
# Main do servidor
# -----------------------
def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    miner_pb2_grpc.add_MinerServicer_to_server(MinerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Miner server running on port {port}. Initial tx=0 created.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
