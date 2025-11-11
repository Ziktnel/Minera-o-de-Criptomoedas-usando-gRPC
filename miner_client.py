import time
import grpc
import hashlib
import random
import string
import miner_pb2
import miner_pb2_grpc

def random_candidate(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def mine_loop(stub, client_id="1", max_attempts=500):
    # pega desafio atual
    info = stub.GetCurrentChallenge(miner_pb2.Empty())
    tx = info.transaction_id
    challenge = info.challenge
    print(f"Transaction {tx} - Challenge {challenge}")

    attempts = 0
    while attempts < max_attempts:
        candidate = random_candidate(24)
        # Opcional: pode usar timestamp + nonce para espaço maior de busca
        sub = miner_pb2.SolutionSubmission(
            transaction_id=tx,
            client_id=str(client_id),
            candidate=candidate
        )
        resp = stub.SubmitSolution(sub)
        attempts += 1

        if resp.accepted:
            print("ENCONTRADO!", resp.message)
            print("Solution:", resp.solution, "Winner:", resp.winner_client_id)
            return True
        # se server respondeu que tx mudou, atualiza info e reinicia
        if "incorreto" in resp.message.lower() or "já solucionado" in resp.message.lower():
            # recarrega desafio atual
            info = stub.GetCurrentChallenge(miner_pb2.Empty())
            tx = info.transaction_id
            challenge = info.challenge
            print("Atualizou para tx", tx, "challenge", challenge)
        # else continuar
    print("Não encontrou em", max_attempts, "tentativas.")
    return False

if __name__ == "__main__":
    channel = grpc.insecure_channel('localhost:50051')
    stub = miner_pb2_grpc.MinerStub(channel)
    mine_loop(stub, client_id="42", max_attempts=50000000)
