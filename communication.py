import socket
import json
import random
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
        "name": f"AImazing{player}",
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

def moveResponse(state):
    """This function generates the response dictionary for a move

    Parameters
    ----------
    state : dict
        state of the game
    Returns
    -------
    str
        json dictionary for the move response
    """
    player = state["current"]
    print(f'-----------{player}----------')
    tile, gate, new_pos = move_test(state)
    move_dict = {
        "tile": tile,
        "gate": gate,
        "new_position": new_pos
    }
    print("---------------------------\nPLAYER {}: {}\n----------------------".format(player, move_dict["new_position"]))
    response_dict = {
        "response": "move",
        "move": move_dict,
        "message": player
    }
    return json.dumps(response_dict)

def saveMessage(player_number, message1, message2=None):
    """This functions saves any message (dictionary) in a .txt file 

    Parameters
    ----------
        player_number (int): number of the player (0 or 1)
        message (dict): message that's going to be saved in the .txt file
    """
    if message2 != None: 
        with open('errors.txt', 'a') as file:
            file.write('LIST OF ERRORS PLAYER {}: {}\n{}\n'.format(player_number, message1, message2))
    else: 
        with open('errors.txt', 'a') as file:
            file.write('LIST OF ERRORS PLAYER {}: {}\n'.format(player_number, message1))
        
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

def get_free_ports(num_ports):
    """Returns a list of `num_ports` available ports on localhost.

    Parameters
    ----------
    num_ports : int
        Number of available ports you want to be listed

    Returns
    -------
    list
        list of the available ports
    """
    ports = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(num_ports):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('', 0))
            port = sock.getsockname()[1]
            ports.append(port)
    return ports

def randomMatricule(quantity, parameter = 4000):
    """This function returns a list of a certain amount of random matricules among 4000 matricules(by default)

    Parameters
    ----------
    quantity : int  
        quantity of random matricules 

    Returns
    -------
    list
        list of the random matricules
    """
    list = []
    matricules = matriculeGenerator(4000)          
    for i in range(quantity):
        i = matricules[random.randint(0, len(matricules))]
        list.append(i)
    return list
        
    
def matriculeGenerator(number):
    """This function generates a certain number of different matricules with 5 digits

    Parameters
    ----------
    number : int
        number of matricules to generate

    Returns
    -------
    list
        list of the different matricules generated
    """
    # Initialize a list of five zeros, which will be used to generate the matricules
    initial = [0, 0, 0, 0, 0]
    # Initialize an empty list that will store the generated matricules
    matricules = []
    # Loop over the range of numbers from 0 to `number`, generating a matricule for each number
    for i in range(number):
        # Generate the matricule based on the value of `i`
        if i < 10:
            initial[4] = i
        elif i >= 10 and i < 100:
            initial[3] = i // 10  # Use integer division to get the tens digit
            initial[4] = i % 10  # Use modulus to get the ones digit
        elif i >= 100 and i < 1000:
            initial[2] = i // 100  # Use integer division to get the hundreds digit
            initial[3] = (i // 10) % 10  # Use integer division and modulus to get the tens digit
            initial[4] = i % 10  # Use modulus to get the ones digit
        elif i >= 1000 and i <= 10000:
            initial[1] = i // 1000  # Use integer division to get the thousands digit
            initial[2] = (i // 100) % 10  # Use integer division and modulus to get the hundreds digit
            initial[3] = (i // 10) % 10  # Use integer division and modulus to get the tens digit
            initial[4] = i % 10  # Use modulus to get the ones digit
        else:
            print("Number too big")
        # Convert the list of digits to a string and append it to the list of matricules
        matricules.append(''.join(map(str, initial)))
    # Return the list of generated matricules
    return matricules


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
                            response = moveResponse(data["state"]).encode()
                            if data["errors"]!=[]:
                                saveMessage(player, data["errors"], "position:{}".format(data["state"]["positions"][data["state"]["current"]]))
                            sendMessage(client, response)
                            data["request"]=""
                        elif data["request"] == 'ping':
                            print(data["request"])
                            client.sendall(pong().encode())
                            print("pong")
                            data["request"]=""
            except socket.timeout:
                pass

