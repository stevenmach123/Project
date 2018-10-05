#
#
# NOTE:
# No peer-to-peer tracker implemented; manual address parameters required
# Not yet tested for > 1 number of connections to server
# Incoming messages will split raw input. Just keep typing to complete the message.
#
#

import socket
import threading

def get_ip(): # Retrieves the IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.google.com', 80))
    ip = s.getsockname()[0] 
    s.close() 
    return ip


class Node:

    def __init__(self):
        self.sockets = [] # keeps a list of all sockets
        self.integrated = threading.Event() # flag to check if we're connected
        self.integrated.clear()
        self.new_message = threading.Event() # flag to check if we received a message
        self.new_message.clear()

    def handler(self, conn, addr): # handles incoming messages
        while True:
            try:
                msg = conn.recv(1024)
                if not msg:                
                    raise ConnectionError # this means the connection was severed
                print("\n<< " + msg.decode()) # print out the message
                self.new_message.set() # set the message flag
                self.send_message(msg, conn) # send message to everyone except the original sender
            except (ConnectionError, OSError):
                print("\n>> " + addr[0] + " disconnected.")
                self.sockets.remove(conn)
                conn.close() # remove the socket from the list
                break

    def disconnect(self): # disconnects from the network
        print("\n>> Disconnecting...")
        [s.close() for s in self.sockets]

    def send_message(self, message, conn=None): # sends a message to all users
        [s.send(message.encode()) for s in self.sockets if not s == conn]


class Server(Node):

    def __init__(self, port):
        super().__init__()
        self.port = port # port to listen on
        self.listen_socket = socket.socket() # socket to listen on
        self.listen_socket.bind(('', self.port))

    def integrate(self): # listens for incoming connections
        self.listen_socket.listen()
        print("Listening for connections...")
        accept_conns_thread = threading.Thread( # thread for accepting connections
            target=self.accept_conns, name="Accept Connections", daemon=True)
        accept_conns_thread.start()

    def accept_conns(self):
        while True:
            try:
                conn, addr = self.listen_socket.accept()  # <-- blocking call
                print("\n" + addr[0] + " has connected.")
                self.integrated.set() # set flag for new connection
                self.sockets.append(conn) 
                handler_thread = threading.Thread(
                    target=self.handler, name="Message Handler", args=(conn, addr), daemon=True)
                handler_thread.start() # start the handler thread
            except OSError:
                pass

    def disconnect(self): # shuts down the listening socket
        super().disconnect()
        self.listen_socket.close()


class Client(Node):

    def __init__(self):
        super().__init__()

    def integrate(self, peer): # connects to a peer
        try:
            conn = socket.socket()
            ip = peer['ip']
            port = peer['port']
            addr = ip, port
            print("Attempting to connect to %s on port %d" %(ip, port))
            conn.connect(addr)
            self.integrated.set() # set the connection flag
            self.sockets.append(conn)
            handler_thread = threading.Thread(
                target=self.handler, name="Message Handler", args=(conn, addr), daemon=True)
            handler_thread.start() # start the handler thread
        except ConnectionError:
            print("Failed to connect to %s" %(ip))
            conn.close()
