import threading
import socket
import sys
import time

from tcp_host_connection import TCPHostConnection

class ConnectionFactory(threading.Thread):

    def __init__(self, name, host, port, commands):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.connections = []
        self.commands = commands
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        print("Starting " + self.name)
        try:
            self.s.bind((self.host,self.port))
        except socket.error as ex:
            print("Bind failed. Errorcode: " + str(ex.errno) + " Message: " + ex.strerror)
            sys.exit()
        else:
            print("Socket bind complete")
            print("Socket created")

        self.s.listen(10)
        print("Socket is now listening on port " + str(self.port))
        while True: # Wait for connections and instantiate a new connection object each time
            connection, address = self.s.accept()
            new_host_connection = TCPHostConnection(address, connection, self.commands)
            self.connections.append(new_host_connection)
            new_host_connection.start()