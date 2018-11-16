import socket
import sys

def main():

    # use the command line args to get the server ip and port
    if len(sys.argv) > 2:
        host = sys.argv[1]
        port = sys.argv[2]
        port = int(port)
