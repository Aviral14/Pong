import socket
import sys
from settings import SERVER_IP, SERVER_PORT

player_no = 0


class Player:
    def connect_to_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("", 0))
            self.port = self.sock.getsockname()[1]
            self.sock.connect((SERVER_IP, SERVER_PORT))
            data = self.sock.recv(1024)
        except Exception as e:
            print(e)
            print(
                "Cannot connect to server! Please Check your internet connection and try again!"
            )
            sys.exit()
        data = data.decode("utf-8")
        ip, port, player_no = data.split(",")
        port = int(port)
        if port:
            self.peer_ip = ip
            self.peer_port = port
            self.connect_to_peer()
        else:
            print("No other players are online Right Now! Please Try Again Later.")
            self.sock.close()
            sys.exit()

    def connect_to_peer(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(("", self.port))
        except Exception as e:
            print(e)
            print(
                "Couldn't Connect to Peer! Connecting Again to the server to find new peer!"
            )
            self.connect_to_server()

class GameState:
    pass