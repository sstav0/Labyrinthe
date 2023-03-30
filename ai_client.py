import socket
import json
import sys
import argparse
from ai import move
from ai import move_test #! temporary test 


def runner_inscription(port: int = 3000):  
    """function that makes the inscription to the game server 
    Parameters
    ----------
    port : int, optional
        _description_, by default 3000
    """
    
    inscription_info: dict = {
        "request": "subscribe",
        "port": args.port,
        "name": "AImazing{}".format(args.player_number),
        "matricules": [args.matricule[0], args.matricule[1]]
    }

    with socket.socket() as s:
        s.connect((args.adresseIP, port))
        info = json.dumps(inscription_info).encode()
        sent = s.sendall(info)
        if sent == len(info):
            print("Inscription envoyée")

        response = json.loads(s.recv(4096).decode())
        ok = response["response"]
        print(f"Received : {ok}")
        
def pong():
    """function that makes the json dictionary response to the "ping" request

    Returns
    -------
    json
       response
    """
    dictPong: dict = {
        "response": "pong"
    }
    pong = json.dumps(dictPong)
    return pong

def moveResponse(state, player):                    #! test function 
    move_dict = {
        "tile": move_test(state, player),
        "gate": move_test(state, player, key="gate"),
        "new_position": move_test(state, player, key="new_pos")
    }
    response_dict = {
        "response": "move",
        "move": move_dict,
        "message": player
    }
    return response_dict
    
        
def server():
    """function that listens on the port that was given in the "runner_inscription" function and sends either "pong" when "ping" is requested or "move" when "play" is requested
    """
    with socket.socket() as s: 
        s.bind((args.adresseIP, args.port))
        s.listen()
        s.settimeout(15)
        while True :
            try :
                client, address = s.accept()
                print("client: {} \nadress: {}".format(client, address))
                with client: 
                    data = json.loads(client.recv(4096).decode())
                    if data["request"] == 'play':
                        print(data["state"])
                        moveResponse(data["state"], args.player_number) #! tries to make a random move with the tests functions => error : the first AI subscribes successfully but the gamer server loses connection with the second AI just after it subscribes "Distant socket closed"
                        data = {}
                    if data["request"] == 'ping':
                        print(data["request"])
                        client.sendall(pong().encode())
                        print("pong")
                        data = {}
            except socket.timeout:
                pass 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--adresseIP', type = str, default = socket.gethostname(), help="Adresse IP à utiliser pour cette version")
    parser.add_argument("--port", type=int, help="Port à utiliser pour cette version")
    parser.add_argument("--player_number", type=int, help="Le numéro du joueur doit être 0 ou 1; 2 IA jouant ensemble ne peuvent pas avoir le même numéro")
    parser.add_argument("--matricule", nargs=2, help="Liste contenant les deux matricules de l'IA")
    args = parser.parse_args()
    
    runner_inscription()
    server()