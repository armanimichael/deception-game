import pygame
import math, time, random, sys, os
from colors import Colors
from screeninfo import get_monitors

pygame.init()
pygame.display.set_caption("A Game of Deception")

RES_LIST = [
    [800 , 600],
    [1024, 768],
    [1280, 800],
    [1680, 1050],
    [1920, 1080]]

MAX_RES = [get_monitors()[0].width, get_monitors()[0].height]
DEF_RES = [800, 600]
RES = RES_LIST[0]
FPS = 10

TOP_LEFT = []
PLAYER = [3, 3]
GRID = []
CELL_COUNT = 10
CELL_SIZE = 0

SELECT = "NONE"

menus = {"MOVE":["MOVE"], "ATTACK":["SHOOT", "KNIFE"], "TRAPS":["ALARM", "PITFALL"], "DETECT":["DETECT"]}
clicked = False

fpsClock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode(RES)#, pygame.FULLSCREEN)


def init():
    global GRID
    
    for i in range(0, CELL_COUNT):
        GRID.append([])
        for j in range(0, CELL_COUNT):
            GRID[i].append([])
    
    GRID[PLAYER[0]][PLAYER[1]].append("PLAYER")

def process():
    global clicked
        
    while True:
        get_input()
        draw()
        clicked = False

def draw():
    DISPLAY.fill(Colors.WHITE)
    dims = RES
    
    draw_grid()
    draw_UI()
    
    pygame.display.update()

def get_input():
    global clicked, RES, DISPLAY, CELL_COUNT, SELECT
    
    # pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_o:
                i = RES_LIST.index(RES)
                if i < len(RES_LIST) - 1:
                    
                    r = RES_LIST[i]
                    if r[0] <= MAX_RES[0] and r[1] <= MAX_RES[1]:
                        RES = RES_LIST[i+1]
                        DISPLAY = pygame.display.set_mode(RES)
            
            if event.key == pygame.K_u:
                i = RES_LIST.index(RES)
                if i > 0:
                    RES = RES_LIST[i-1]
                    DISPLAY = pygame.display.set_mode(RES)
            
            if event.key == pygame.K_j:
                if CELL_COUNT >= 4: CELL_COUNT -= 1
            
            if event.key == pygame.K_k:
                if CELL_COUNT < 16: CELL_COUNT += 1
            
            if event.key == pygame.K_ESCAPE:
                if SELECT == "NONE": quit()
                else: SELECT = "NONE"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True

def hover(bot_right):
    mouse = pygame.mouse.get_pos()
    
    if bot_right[0] > mouse[0] > TOP_LEFT[0] and bot_right[1] > mouse[1] > TOP_LEFT[1]:
        cell = cell_center(mouse)
        t = [(cell[0]*CELL_SIZE + TOP_LEFT[0]),
             (cell[1]*CELL_SIZE + TOP_LEFT[1])]
        
        bg = pygame.Rect(t[0], t[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY, Colors.LIGHT_GRAY, bg)
        
        if clicked:
            cell_click(cell)


def menu_click(m):
    global SELECT
    # "MOVE", "ATTACK", "TRAPS", "DETECT"
    
    if SELECT == m: SELECT = "NONE"
    else: SELECT = m

def cell_click(cell):
    global PLAYER, GRID
    
    tmp  = [[PLAYER[0], PLAYER[1]-1], [PLAYER[0], PLAYER[1]+1], [PLAYER[0]+1, PLAYER[1]], [PLAYER[0]-1, PLAYER[1]]]        
    if cell in tmp:
        if SELECT == "MOVE":
            # in Server/Client Version: communicate with server (PlayerPos, MovePos) for check, then get the new PlayerPos
            
            GRID[cell[0]][cell[1]].append("PLAYER")
            GRID[PLAYER[0]][PLAYER[1]].remove("PLAYER")
            
            PLAYER = cell        
        
        elif SELECT in menus["TRAPS"]:
            # in Server/Client Version: communicate with server (PlayerPos, TrapPos) to place Traps
            GRID[cell[0]][cell[1]].append(SELECT)

def cell_center(pos):
    x, y = pos
    
    x = int((x - TOP_LEFT[0]) / CELL_SIZE)
    y = int((y - TOP_LEFT[1]) / CELL_SIZE)
    
    return [x, y]

def quit():
    pygame.quit()
    sys.exit()


def draw_grid():
    global TOP_LEFT, CELL_SIZE
    
    CELL_SIZE = int(RES[1] * .75 / CELL_COUNT)
    TOP_LEFT = [
        int(RES[0]/2 - (CELL_COUNT/2 * CELL_SIZE)),
        int(RES[1] * .15 / 2)]
    
    bot_right = [(c + CELL_SIZE*CELL_COUNT) for c in TOP_LEFT]
    hover(bot_right)
    
    for r in range(0, CELL_COUNT):
        for c in range(0, CELL_COUNT):
            x, y = [(TOP_LEFT[0] + CELL_SIZE*c), (TOP_LEFT[1] + CELL_SIZE*r)]
            
            objs = GRID[c][r]
            txt  = ""
            p    = False
            
            if objs != []:
                for e in objs:
                    if   e == "PLAYER" : p = True; txt = ""
                    elif e == "PITFALL": txt = "X"
                    elif e == "ALARM"  : txt = "A"
            
            if txt != "": draw_text(txt, int(CELL_SIZE*2/3), [int(x + CELL_SIZE/2), int(y + CELL_SIZE/2)])
            pygame.draw.rect(DISPLAY, Colors.BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            if p: draw_player(x, y, CELL_SIZE)
    
    bg = pygame.Rect(TOP_LEFT[0], TOP_LEFT[1], CELL_SIZE * CELL_COUNT, CELL_SIZE * CELL_COUNT)
    pygame.draw.rect(DISPLAY, Colors.BLACK, bg, 3)

def draw_UI():
    width  = int(RES[0] / len(menus))
    height = int(RES[0] / 15)
    
    y = RES[1] - height
    i = 0
    
    draw_text(SELECT, 15, [35, y - 10])
    
    for m in menus:
        x = i * width
        
        button(m, x, y, width, height, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, menu_click, m)
        i += 1
    
    if SELECT == "ATTACK" or SELECT == "TRAPS":
        if SELECT == "ATTACK": x = width
        if SELECT == "TRAPS": x = width * 2
        
        y = RES[1] - height
        height = int(height * 3/4)
        
        for sub in menus[SELECT]:
            y -= (height)
            button(sub, x, y, int(width * 3/4), height, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, menu_click, sub)

def draw_player(x, y, size):
    x = int(x + size/2)
    y = int(y + size/2)
    
    size = int(size * 1/3)
    
    bg = pygame.Rect(0, 0, size, size)
    bg.center = [x, y]
    pygame.draw.rect(DISPLAY, Colors.BLACK, bg)


def button(msg, x, y, w, h, rgb, h_rgb, b_rgb, action=None, args=[], border=3, t_dim=20, t_rgb=Colors.BLACK):
    coords = [int(c) for c in (x, y, w, h)]
    color = rgb
    
    if action != None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            color = h_rgb
            if click[0] and action != None and clicked:
                if args == []: action()
                else: action(args)
    
    pygame.draw.rect(DISPLAY, color, coords)
    pygame.draw.rect(DISPLAY, b_rgb, coords, border)
    
    draw_text(msg, t_dim, (int(x + (w/2)), int(y + (h/2))))

def draw_text(msg, h, coords, color=Colors.BLACK):
    font = pygame.font.Font("freesansbold.ttf", h)   
    textSurf = font.render(msg, True, color)
    textRect = textSurf.get_rect()
    textRect.center = [int(c) for c in coords]
    DISPLAY.blit(textSurf, textRect)

def drawRegularPolygon(surface, color, numSides, tiltAngle, x, y, radius):
    pts = []
    for i in range(numSides):
        x = x + radius * math.cos(tiltAngle + math.pi * 2 * i / numSides)
        y = y + radius * math.sin(tiltAngle + math.pi * 2 * i / numSides)
        pts.append([int(x), int(y)])
    pygame.draw.polygon(surface, color, pts)



init()
process()
