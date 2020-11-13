
import pygame, socket
import time, sys


pygame.init()
pygame.display.set_caption("A Game of Deception")

FPS = 30
RES = [800, 600] # [get_monitors()[0].width, get_monitors()[0].height]

fpsClock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode(RES)#, pygame.FULLSCREEN)


def game_loop():
    while True:       
        fpsClock.tick(FPS)


IP   = "localhost"
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, port))

mysend(s, b'Ciao Bitch, questo essere un messaggio')
game_loop()




def mysend(sock, msg):
    totalsent = 0
    
    while totalsent < len(msg):
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent



class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
