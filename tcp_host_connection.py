import threading
import pickle

class TCPHostConnection(threading.Thread):
    
    def __init__(self, address, connection, commands):
        threading.Thread.__init__(self)
        self.address = address[0]
        self.port = address[1]
        self.connection = connection
        self.commands = commands

    def run(self):
        print("Connected with " + self.address + " on port " + str(self.port))
        while True:
            data = self.receive()
            requested_command = data['command']
            params = data['params']
            action = self.commands[requested_command]
            if params:
                reply = action(params)
            else:
                reply = action()
            self.send(reply)
    
    def receive(self):
        binary_data = self.connection.recv(1024)
        data = pickle.loads(binary_data)
        return data

    def send(self, data):
        binary_data = pickle.dumps(data)
        self.connection.send(binary_data)
