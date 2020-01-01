import pygame
import socket
import sys


class Player:
    
    def connect_to_server(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER_IP="127.0.0.1"
        SERVER_PORT= 8000
        try:
            sock.connect((SERVER_IP,SERVER_PORT))
            data = sock.recv(1024)
        except:
            print("Cannot connect to server! Please Check your internet connection and try again!")
            sys.exit()
        data=data.decode("utf-8")
        ip,port=data.split(",")
        port=int(port)
        if port:
            self.peer_ip=ip
            self.peer_port=port
        else:
            print("No other players are online Right Now! Please Try Again Later.")
            sys.exit()

if __name__=='__main__':
    player=Player()
    player.connect_to_server()