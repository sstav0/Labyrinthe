import socket
import json
import argparse
from ai import move
from ai import move_test #! temporary test 


def runner_inscription(adresseIP, portClient, player, matricules, port: int = 3000):  
    """function that makes the inscription to the game server 
    Parameters
    ----------
    port : int, optional
        _description_, by default 3000
    """
    
    inscription_info: dict = {
        "request": "subscribe",
        "port": portClient,
        "name": "AImazing{}".format(player),
        "matricules": [matricules[0], matricules[1]]
    }

    with socket.socket() as s:
        s.connect((adresseIP, port))
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

def moveResponse(state, player):
    """This function generates the response dictionary for a move

    Parameters
    ----------
    state : dict
        state of the game
    player : int
        number of the player

    Returns
    -------
    str
        json dictionary for the move response
    """
    move_dict = {
        "tile": move_test(state, player,"tile"),
        "gate": move_test(state, player,"gate"),
        "new_position": move_test(state, player,"new_pos")
    }
    print("---------------------------\nPLAYER {}: {}\n----------------------".format(player, move_dict["new_position"]))
    response_dict = {
        "response": "move",
        "move": move_dict,
        "message": player
    }
    return json.dumps(response_dict)

def saveMessage(player_number, message):
    """This functions saves any message (dictionary) in a .txt file 

    Parameters
    ----------
        player_number (int): number of the player (0 or 1)
        message (dict): message that's going to be saved in the .txt file
    """
    with open('errors.txt', 'a') as file:
        file.write('LIST OF ERRORS PLAYER {}: {}\n'.format(player_number, message))
    
def sendMessage(socket, message): 
    """This functions sends a message on a socket 

    Parameters
    ----------
    socket : 
        The socket on which the message is sent     
    message : str
        The json dictionary containing the message 
    """
    totalSent = 0
    while totalSent < len(message):
        sent = socket.send(message[totalSent:])
        totalSent += sent

def receiveMessage(socket):
    """This function receives a message sent on a socket

    Parameters
    ----------
    socket : socket
        the socket on which the message has been send 

    Returns
    -------
    _type_
        -
    """
    msg =""
    received = False 
    while not received : 
        try : 
            msg +=socket.recv(4096).decode()
        except socket.timeout:
            received = True
    return msg
        
        
def server(adresseIP, port, player, serv_timeout = 1, client_timeout = 0.2):
    with socket.socket() as s: 
        s.bind((adresseIP, port))           
        s.listen()
        s.settimeout(serv_timeout)
        while True :
            try : 
                client, address = s.accept()
                client.settimeout(client_timeout)
                with client:
                    msg =""
                    received = False
                    while not received:
                        try:
                            msg+=client.recv(4096).decode()
                        except socket.timeout:
                            received = True
                    if msg!="":
                        data = json.loads(msg)
                        if data["request"] == 'play':
                            print(data["request"])
                            response = moveResponse(data["state"], player).encode()
                            saveMessage(player, response)
                            sendMessage(client, response)
                            data["request"]=""
                        elif data["request"] == 'ping':
                            print(data["request"])
                            client.sendall(pong().encode())
                            print("pong")
                            data["request"]=""
            except socket.timeout:
                pass

