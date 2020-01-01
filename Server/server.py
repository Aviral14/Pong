import socketserver
import time
import threading
import settings

connected_clients = []


def make_pair():
    while 1:
        if len(connected_clients) >= 2:
            client1 = connected_clients.pop(0)
            client2 = connected_clients.pop(0)
            client1.fix_match(client2.client_address)
            client2.fix_match(client1.client_address)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Class to implement multithreaded TCP Server"""

    pass


class TCPHandler(socketserver.BaseRequestHandler):
    """Class to handle requests from each client"""

    def handle(self):
        connected_clients.append(self)
        t = time.process_time()
        while 1:
            if time.process_time() - t >= 30:
                msg = "0,0"
                self.request.sendall(msg.encode())
                connected_clients.remove(self)
                break
            if  not any(obj for obj in connected_clients if obj == self):
                break

    def fix_match(self, addr):
        ip, port = addr
        msg = f"{ip},{port}"
        self.request.sendall(msg.encode())


if __name__ == "__main__":
    server = ThreadedTCPServer(
        (settings.HOST_ADDRESS, settings.HOST_PORT), TCPHandler
    )
    connection_thread = threading.Thread(target=server.serve_forever)
    matching_thread = threading.Thread(target=make_pair)
    connection_thread.start()
    matching_thread.start()