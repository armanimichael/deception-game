import pygame
import math, time, random, sys, os
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

MENUS = {"MOVE":["MOVE"],
         "ATTACK":["SHOOT", "KNIFE"],
         "TRAPS":["ALARM", "PITFALL"],
         "DETECT":["DETECT"]}

class Game:
    def __init__(self, c):
        self.RES = RES_LIST[0]
        self.DISPLAY = pygame.display.set_mode(self.RES)

        self.player_pos = [3, 3]
        self.GRID = []
        
        self.cell_count = 10
        self.cell_size = 0
        self.top_left = []

        self.select = "NONE"
        self.clicked = False
        
        self.play = True
        self.connection = c

        
        for i in range(0, self.cell_count):
            self.GRID.append([])
            for j in range(0, self.cell_count):
                self.GRID[i].append([])
        
        self.GRID[self.player_pos[0]][self.player_pos[1]].append("PLAYER")
    
    def process(self):
        self.get_input()
        self.draw()
        
        self.clicked = False


    def draw(self):
        self.DISPLAY.fill(Colors.WHITE)
        dims = self.RES
        
        self.draw_grid()
        self.draw_UI()
        
        pygame.display.update()

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
            
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
                
                if event.key == pygame.K_j:
                    if self.cell_count >= 4: self.cell_count -= 1
                
                if event.key == pygame.K_k:
                    if self.cell_count < 16: self.cell_count += 1
                
                if event.key == pygame.K_ESCAPE:
                    if self.select == "NONE": self.play = False
                    else: self.select = "NONE"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
    
    
    def hover(self, bot_right):
        mouse = pygame.mouse.get_pos()
        
        if bot_right[0] > mouse[0] > self.top_left[0] and bot_right[1] > mouse[1] > self.top_left[1]:
            cell = self.cell_center(mouse)
            t = [(cell[0]*self.cell_size + self.top_left[0]),
                (cell[1]*self.cell_size + self.top_left[1])]
            
            bg = pygame.Rect(t[0], t[1], self.cell_size, self.cell_size)
            pygame.draw.rect(self.DISPLAY, Colors.LIGHT_GRAY, bg)
            
            if self.clicked:
                self.cell_click(cell)

    def menu_click(self, m):
        # "MOVE", "ATTACK", "TRAPS", "DETECT"
        
        if self.select == m: self.select = "NONE"
        else: self.select = m

    def cell_click(self, cell):
        tmp  = [[self.player_pos[0], self.player_pos[1]-1], 
                [self.player_pos[0], self.player_pos[1]+1], 
                [self.player_pos[0]+1, self.player_pos[1]], 
                [self.player_pos[0]-1, self.player_pos[1]]]
        
        if cell in tmp:
            if self.select == "MOVE":
                # in Server/Client Version: communicate with server (PlayerPos, MovePos) for check, then get the new PlayerPos
                
                self.GRID[cell[0]][cell[1]].append("PLAYER")
                self.GRID[self.player_pos[0]][self.player_pos[1]].remove("PLAYER")
                
                self.player_pos = cell        
            
            elif self.select in MENUS["TRAPS"]:
                # in Server/Client Version: communicate with server (PlayerPos, TrapPos) to place Traps
                self.GRID[cell[0]][cell[1]].append(self.select)

    def cell_center(self, pos):
        x, y = pos
        
        x = int((x - self.top_left[0]) / self.cell_size)
        y = int((y - self.top_left[1]) / self.cell_size)
        
        return [x, y]
    

    def draw_grid(self):
        self.cell_size = int(self.RES[1] * .75 / self.cell_count)
        self.top_left = [
            int(self.RES[0]/2 - (self.cell_count/2 * self.cell_size)),
            int(self.RES[1] * .15 / 2)]
        
        bot_right = [(c + self.cell_size*self.cell_count) for c in self.top_left]
        self.hover(bot_right)
        
        for r in range(0, self.cell_count):
            for c in range(0, self.cell_count):
                x, y = [(self.top_left[0] + self.cell_size*c), (self.top_left[1] + self.cell_size*r)]
                
                objs = self.GRID[c][r]
                txt  = ""
                p    = False
                
                if objs != []:
                    for e in objs:
                        if   e == "PLAYER" : p = True; txt = ""
                        elif e == "PITFALL": txt = "X"
                        elif e == "ALARM"  : txt = "A"
                
                if txt != "": Draw.draw_text(self.DISPLAY, txt, int(self.cell_size*2/3), [int(x + self.cell_size/2), int(y + self.cell_size/2)])
                pygame.draw.rect(self.DISPLAY, Colors.BLACK, (x, y, self.cell_size, self.cell_size), 1)
                if p: self.draw_player(x, y, self.cell_size)
        
        bg = pygame.Rect(self.top_left[0], self.top_left[1], self.cell_size * self.cell_count, self.cell_size * self.cell_count)
        pygame.draw.rect(self.DISPLAY, Colors.BLACK, bg, 3)

    def draw_UI(self):
        width  = int(self.RES[0] / len(MENUS))
        height = int(self.RES[0] / 15)
        
        y = self.RES[1] - height
        i = 0
        
        Draw.draw_text(self.DISPLAY, self.select, 15, [35, y - 10])
        
        for m in MENUS:
            x = i * width
            
            Draw.button(self.DISPLAY, m, x, y, width, height, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.menu_click, self.clicked, m)
            i += 1
        
        if self.select == "ATTACK" or self.select == "TRAPS":
            if self.select == "ATTACK": x = width
            if self.select == "TRAPS": x = width * 2
            
            y = self.RES[1] - height
            height = int(height * 3/4)
            
            for sub in MENUS[self.select]:
                y -= (height)
                Draw.button(self.DISPLAY, sub, x, y, int(width * 3/4), height, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.menu_click, self.clicked, sub)

    def draw_player(self, x, y, size):
        x = int(x + size/2)
        y = int(y + size/2)
        
        size = int(size * 1/3)
        
        bg = pygame.Rect(0, 0, size, size)
        bg.center = [x, y]
        pygame.draw.rect(self.DISPLAY, Colors.BLACK, bg)
    
