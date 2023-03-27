import socket
import json


def runner_inscription(port: int = 3000):
    inscription_info: dict = {
        "request": "subscribe",
        "port": 5000,
        "name": "AImazing",
        "matricules": ["21151", "21211"]
    }

    with socket.socket() as s:
        s.connect((socket.gethostname(), port))

        info = json.dumps(inscription_info).encode()
        sent = s.sendall(info)
        if sent == len(info):
            print("Inscription envoyée")

        response = json.loads(s.recv(4096).decode())
        ok = response["response"]
        print(f"Reçu : {ok}")

def daccord():
    print('daccord')

if __name__ == '__main__':
    runner_inscription()
