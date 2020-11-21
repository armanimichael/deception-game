
import pygame, socket
import time, sys

from game import Game
from menu import Menu
from client import Client

pygame.init()
pygame.display.set_caption("A Game of Deception")

FPS = 30
fpsClock = pygame.time.Clock()

c = Client()
MENU = Menu(c)

def main_loop():
    while True:
        menu_loop()
        game_loop()
        
        MENU.reset_menu()


def menu_loop():
    while MENU.play:
        MENU.process()
        fpsClock.tick(FPS)

def game_loop():
    info = {"SERVER":MENU.server_process, "CONNECTION":c}

    GAME = Game(info)
    while GAME.play:
        GAME.process()
        fpsClock.tick(FPS)


main_loop()
