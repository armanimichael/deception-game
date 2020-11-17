
import pygame, socket
import time, sys

from game import Game
from menu import Menu

pygame.init()
pygame.display.set_caption("A Game of Deception")

FPS = 30
fpsClock = pygame.time.Clock()

MENU = Menu()

def main_loop():
    while True:
        menu_loop()
        game_loop()
        
        MENU.play = True

def menu_loop():
    while MENU.play:
        MENU.process()
        fpsClock.tick(FPS)

def game_loop():
    GAME = Game()
    while GAME.play:
        GAME.process()
        fpsClock.tick(FPS)


main_loop()
