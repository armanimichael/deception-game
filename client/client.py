import socket, json

class Client:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def conn(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        sent = self.sock.send(msg)
        if sent == 0: raise RuntimeError("Socket Connection Broken")

    def recv(self):
        msg = self.sock.recv(2048)

        if msg == b'': raise RuntimeError("Socket Connection Broken")
        else: return json.loads(msg)
    
    def close(self):
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)