import socket
import json


def runner_inscription():
    port: int = 5000

    inscription_info: dict = {
        "request": "subscribe",
        "port": port,
        "name": "GPETE",
        "matricules": ["21151", "21211"]
    }

    with socket.socket() as s:
        s.connect((socket.gethostname(), port))

        info = json.dumps(inscription_info).encode()
        sent = s.sendall(info)
        if sent == len(info):
            print("Inscription envoyée")

        response = s.recv(4096).decode()
        print(f"Reçu : {response}")
