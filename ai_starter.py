from communication import runner_inscription, randomMatricule, server, get_free_ports
import argparse
import socket

# socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--IPaddress', type=str, default=socket.gethostbyname(socket.gethostname()),
                        help="IP address of this AI version")
    parser.add_argument('--aiNumber', type=int, default=2,
                        help="The number of AI to run simultaneously, number must be even")
    args = parser.parse_args()

    ports = get_free_ports(10)
    runner_inscription(
        args.IPaddress, ports[args.aiNumber], args.aiNumber, randomMatricule(2))
    server(ports[args.aiNumber], args.aiNumber)
