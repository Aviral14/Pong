import socketserver
import time
import threading
import settings

connected_clients = []


def make_pair():
    global connected_clients
    while True:
        if len(connected_clients) >= 2:
            client1, client2 = connected_clients[:2]
            client1.fix_match(client2.client_address, player_no=1)
            client2.fix_match(client1.client_address, player_no=2)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Class to implement multithreaded TCP Server"""

    pass


class TCPHandler(socketserver.BaseRequestHandler):
    """Class to handle requests from each client"""

    def handle(self):
        connected_clients.append(self)
        t = time.process_time()
        while True:
            if time.process_time() - t >= 30:
                msg = "0,0,0"
                self.request.send(msg.encode())
                connected_clients.remove(self)
                break
            if not [obj for obj in connected_clients if obj == self]:
                break
        self.request.close()

    def fix_match(self, addr, player_no):
        ip, port = addr
        msg = f"{ip},{port},{player_no}"
        self.request.send(msg.encode())
        connected_clients.pop(0)


if __name__ == "__main__":
    server = ThreadedTCPServer((settings.HOST_ADDRESS, settings.HOST_PORT), TCPHandler)
    connection_thread = threading.Thread(target=server.serve_forever)
    matching_thread = threading.Thread(target=make_pair)
    connection_thread.start()
    matching_thread.start()
