
import communication
import argparse
import socket



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--IPaddress', type=str, default = socket.gethostbyname(socket.gethostname()), help="IP address of this AI version")
    parser.add_argument("--port", type=int, help="Port to use for this AI version")
    parser.add_argument("--player", type=int)
    parser.add_argument("--matricules", nargs=2)
    args = parser.parse_args()
    
    communication.runner_inscription(args.IPaddress, args.port, args.player, args.matricules)
    communication.server(args.IPaddress, args.port, args.player)
    
    
