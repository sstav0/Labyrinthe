
import communication
import argparse
import socket


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--adresseIP', type = str, default = socket.gethostname(), help="Adresse IP à utiliser pour cette version")
    parser.add_argument("--port", type=int, help="Port à utiliser pour cette version")
    parser.add_argument("--player", type=int, help="Le numéro du joueur doit être 0 ou 1; 2 IA jouant ensemble ne peuvent pas avoir le même numéro")
    parser.add_argument("--matricules", nargs=2, help="Liste contenant les deux matricules de l'IA")
    args = parser.parse_args()
    
    communication.runner_inscription(args.adresseIP, args.port, args.player, args.matricules)
    communication.server(args.adresseIP, args.port, args.player)