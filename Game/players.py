import socket
import sys
import time
import threading
from settings import SERVER_IP, SERVER_PORT, TIMEOUT_PERIOD, ACK_PERIOD

# Game state is a combination of OP_CODE and necessary variable values to correctly
# define the action undertaken by the player/opponent. A single value follows
# the OP_CODE-"OP_MOVE" which denotes the y co-ordinate of top left corner of the
# player's/opponent's bar while a tuple with three values-
# (x component,y component (of velocity of ball after hitting),y co-ordinate of bar)
# follows the OP_CODE-"OP_HIT" .

player_game_state = None
player_game_state_update = False
opponent_game_state = None
opponent_game_state_update = False
player_no = 0
going = True


class Player:
    def connect_to_server(self):
        global player_no
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("", 0))
            self.ip, self.port = self.sock.getsockname()
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
        player_no = int(player_no)
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
            self.sock.bind((self.ip, self.port))
            self.sock.settimeout(TIMEOUT_PERIOD)
        except Exception as e:
            print(e)
            print(
                "Couldn't Connect to Peer! Connecting Again to the server to find new peer!"
            )
            self.connect_to_server()

    def receive_data(self):
        global opponent_game_state
        global opponent_game_state_update
        global going
        try:
            while going:
                msg = self.sock.recvfrom(1024)
                val, addr = msg
                data = val.decode("utf-8")
                if data != "Alive":
                    opponent_game_state = data
                    opponent_game_state_update = True
        except socket.timeout as e:
            print(e)
            print("The Opponent seems to have Disconnected.You Won!")

    def send_data(self):
        global player_game_state
        global player_game_state_update
        global going
        while going:
            if player_game_state_update:
                self.sock.sendto(
                    player_game_state.encode("utf-8"), (self.peer_ip, self.peer_port)
                )
                player_game_state_update = False

    def send_ack_msg(self):
        global going
        while going:
            time.sleep(ACK_PERIOD)
            self.sock.sendto("Alive".encode("utf-8"), (self.peer_ip, self.peer_port))

    def run(self):
        receive_thread = threading.Thread(target=self.receive_data)
        send_thread = threading.Thread(target=self.send_data)
        send_ack_thread = threading.Thread(target=self.send_ack_msg)
        receive_thread.start()
        send_thread.start()
        send_ack_thread.start()
