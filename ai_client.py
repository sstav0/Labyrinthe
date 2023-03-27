import socket
import json
import sys
#import ai


def runner_inscription(port: int = 3000):  
    """function that makes the inscription to the game server 
    Parameters
    ----------
    port : int, optional
        _description_, by default 3000
    """
    global infos
    global serverPort
    
    infos = sys.stdin.readline().rstrip("\n").split(" ")  #!Pouvoir mettre directement le numéro de port après le fichier dans le terminal
    serverPort = int(infos[0])
    number = int(infos[1])                  #* number of the IA version
    matricules = (infos[2], infos[3])
    
    inscription_info: dict = {
        "request": "subscribe",
        "port": int(infos[0]),
        "name": "AImazing{}".format(int(infos[1])),
        "matricules": [matricules[0], matricules[1]]
    }

    with socket.socket() as s:
        s.connect((socket.gethostname(), port))

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
    

#def play(port: int = 3000): 
    
        
def server():
    """function that listens on the port that was given in the "runner_inscription" function and sends either "pong" when "ping" is requested or "move" when "play" is requested
    """
    with socket.socket() as s: 
        s.bind((socket.gethostname(), serverPort))
        s.listen()
        s.settimeout(0.5)
        while True :
            try :
                client, address = s.accept()
                print("client: {} \nadress: {}".format(client, address))
                with client: 
                    data = json.loads(client.recv(4096).decode())
                    if data["request"] == 'play':
                        print('play')
                        data = None
                    if data["request"] == 'ping':
                        print(data["request"])
                        client.sendall(pong().encode())
                        print("pong")
                        data = None
            except socket.timeout:
                pass 


if __name__ == '__main__':
    runner_inscription()
    server()