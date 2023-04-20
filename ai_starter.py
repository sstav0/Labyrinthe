from communication import runner_inscription
from communication import randomMatricule
from communication import server
from communication import get_free_ports
import argparse
import socket



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--IPaddress', type=str, default="172.17.10.59", help="IP address of this AI version")
    parser.add_argument('--aiNumber', type=int, default=2, help="The number of AI to run simultaneously, number must be even")
    args = parser.parse_args()
    
    ports = get_free_ports(10)
    runner_inscription(args.IPaddress, ports[args.aiNumber], args.aiNumber, randomMatricule(2))
    server(args.IPaddress, ports[args.aiNumber], args.aiNumber)