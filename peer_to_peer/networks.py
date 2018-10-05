#
#
# NOTE:
# No peer-to-peer tracker implemented; manual address parameters required
# Not yet tested for > 1 number of connections to server
# 

import socket
import threading

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class Node:

    def __init__(self):
        self.sockets = []
        self.integrated = threading.Event()
        self.integrated.clear()
        self.new_message = threading.Event()
        self.new_message.clear()

    def handler(self, conn, addr):
        while True:
            try:
                msg = conn.recv(1024)
                if not msg:
                    raise ConnectionError
                print("\n<< " + msg.decode())
                self.new_message.set()
                self.send_message(msg, conn)
            except (ConnectionError, OSError):
                print("\n>> " + addr[0] + " disconnected.")
                self.sockets.remove(conn)
                conn.close()
                break

    def disconnect(self):
        print("\n>> Disconnecting...")
        [s.close() for s in self.sockets]

    def send_message(self, message, conn=None):
        [s.send(message.encode()) for s in self.sockets if not s == conn]


class Server(Node):

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.listen_socket = socket.socket()
        self.listen_socket.bind(('', self.port))

    def integrate(self):
        self.listen_socket.listen()
        print("Listening for connections...")
        accept_conns_thread = threading.Thread(
            target=self.accept_conns, name="Accept Connections", daemon=True)
        accept_conns_thread.start()

    def accept_conns(self):
        while True:
            try:
                conn, addr = self.listen_socket.accept()  # <-- blocking call
                print("\n" + addr[0] + " has connected.")
                self.integrated.set()
                self.sockets.append(conn)
                handler_thread = threading.Thread(
                    target=self.handler, name="Message Handler", args=(conn, addr), daemon=True)
                handler_thread.start()
            except OSError:
                pass

    def disconnect(self):
        super().disconnect()
        self.listen_socket.close()


class Client(Node):

    def __init__(self):
        super().__init__()

    def integrate(self, peer):
        try:
            conn = socket.socket()
            ip = peer['ip']
            port = peer['port']
            addr = ip, port
            print("Attempting to connect to %s on port %d" %(ip, port))
            conn.connect(addr)
            self.integrated.set()
            self.sockets.append(conn)
            handler_thread = threading.Thread(
                target=self.handler, name="Message Handler", args=(conn, addr), daemon=True)
            handler_thread.start()
        except ConnectionError:
            conn.close()
