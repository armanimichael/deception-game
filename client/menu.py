import pygame
import math, time, random, sys, os, asyncio
from screeninfo import get_monitors

from colors import Colors
from draw import DrawHandler as Draw

RES_LIST = [
    [800 , 600],
    [1024, 768],
    [1280, 800],
    [1680, 1050],
    [1920, 1080]]
MAX_RES = [get_monitors()[0].width, get_monitors()[0].height]

class Menu:
    def __init__(self, c):
        self.clicked = False
        self.screen = "MAIN_MENU" #MAIN_MENU, SETTINGS_MENU, CREDITS_SCREEN, CREATING_SERVER, CONNECTING_TO_SERVER
        
        self.RES = RES_LIST[0]
        self.DISPLAY = pygame.display.set_mode(self.RES)#, pygame.FULLSCREEN)

        self.play = True
        self.connection = c


    def process(self):
        self.get_input()
        self.draw()
        self.clicked = False


    def draw(self):
        self.DISPLAY.fill(Colors.WHITE)
        dims = self.RES
        
        # Draw Main Menu:
        if self.screen == "MAIN_MENU":
            x, y = [dims[0]/4, dims[1]/3]
            w, h = [x * 2, (y / 3 - 15)]
            
            # button(msg, x, y, w, h, rgb, h_rgb, b_rgb)
            
            Draw.button(self.DISPLAY, "Join Game", x, y, w, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "CONNECTING_TO_SERVER")
            
            y += y/3
            Draw.button(self.DISPLAY, "Host Game", x, y, w, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "CREATING_SERVER")
            
            y += y/3
            Draw.button(self.DISPLAY, "Settings" , x, y, w/2 - 5, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "MAIN_MENU")
            Draw.button(self.DISPLAY, "Credits"  , x + w/2 + 5, y, w/2, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "MAIN_MENU")
        
        elif self.screen == "CONNECTING_TO_SERVER":
            Draw.draw_text(self.DISPLAY, "SEARCHING FOR SERVER...", 50, [dims[0]/2, dims[1]/2])
        
        elif self.screen == "CREATING_SERVER":
            Draw.draw_text(self.DISPLAY, "LOADING SERVER...", 50, [dims[0]/2, dims[1]/2])
        
        pygame.display.update()


    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    i = RES_LIST.index(self.RES)
                    if i < len(RES_LIST) - 1:
                        
                        r = RES_LIST[i]
                        if r[0] <= MAX_RES[0] and r[1] <= MAX_RES[1]:
                            self.RES = RES_LIST[i+1]
                            self.DISPLAY = pygame.display.set_mode(self.RES)
                
                if event.key == pygame.K_u:
                    i = RES_LIST.index(self.RES)
                    if i > 0:
                        self.RES = RES_LIST[i-1]
                        self.DISPLAY = pygame.display.set_mode(self.RES)
                    
                
                if event.key == pygame.K_ESCAPE:
                    if self.screen != "MAIN_MENU": screen = "MAIN_MENU"
                    else: quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True


    def screen_change(self, t):
        self.screen = t
        
        if self.screen == "CREATING_SERVER":
            error = False

            # Create Server
            try: subprocess.run("../server/main")
            except:
                error = True
                print("COULD NOT CREATE SERVER")
            
            # Connect to Server
            if not error:
                self.connection.conn("localhost", 1234)
                self.connection.send(b'{"username":"Zampa"}')

                res = self.connection.recv()
                if res["result"] == success:
                    self.play = False
                    self.DISPLAY = pygame.display.set_mode(self.RES)
                else: print("ERROR")

            self.screen = "MAIN_MENU"
        
        
        if self.screen == "CONNECTING_TO_SERVER":
            error = False

            # Connect to Server
            try: self.connection.conn("localhost", 1234)
            except: error = True

            if not error:
                self.connection.send(b'{"username":"Zampa2S"}')

                res = self.connection.recv()
                if res["result"] == "success":
                    self.play = False
                    self.DISPLAY = pygame.display.set_mode(self.RES)
                else: print("ERROR")

            self.screen = "MAIN_MENU"