
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
DEF_RES = RES_LIST[0]
RES = RES_LIST[2]
FPS = 30

clicked = False
screen = "MAIN_MENU" #MAIN_MENU, SETTINGS_MENU, CREDITS_SCREEN, CREATING_SERVER, CONNECTING_TO_SERVER
delta = [1, 1]

fpsClock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode(RES)#, pygame.FULLSCREEN)


def process():
    global clicked
        
    while True:
        get_input()
        get_delta()
        
        draw()        
        clicked = False


def draw():
    DISPLAY.fill(Colors.WHITE)
    dims = RES
    
    # Draw Main Menu:
    if screen == "MAIN_MENU":
        x, y = [dims[0]/4, dims[1]/3]
        w, h = [x * 2, (y / 3 - 15)]
        
        # button(msg, x, y, w, h, rgb, h_rgb, b_rgb)
        
        button("Join Game", x, y, w, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, screen_change, "CONNECTING_TO_SERVER")
        
        y += y/3
        button("Host Game", x, y, w, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, screen_change, "CREATING_SERVER")
        
        y += y/3
        button("Settings" , x, y, w/2 - 5, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, screen_change, "MAIN_MENU")
        button("Credits"  , x + w/2 + 5, y, w/2, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, screen_change, "MAIN_MENU")
    
    elif screen == "CONNECTING_TO_SERVER":
        draw_text("SEARCHING FOR SERVER...", 50, [dims[0]/2, dims[1]/2])
    
    elif screen == "CREATING_SERVER":
        draw_text("LOADING SERVER...", 50, [dims[0]/2, dims[1]/2])
    
    pygame.display.update()


def button(msg, x, y, w, h, rgb, h_rgb, b_rgb, action=None, args=[], t_dim=20, t_rgb=Colors.BLACK):
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
    pygame.draw.rect(DISPLAY, b_rgb, coords, 3)
    
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


def get_input():
    global clicked, screen, RES, DISPLAY
    
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
                
            
            if event.key == pygame.K_ESCAPE:
                print(RES)
                quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True


def get_delta():
    global delta
    
    if RES != DEF_RES:
        delta[0] = RES[0] / DEF_RES[0]
        delta[1] = RES[1] / DEF_RES[1]
    else: delta = [1, 1]

def quit():
    pygame.quit()
    sys.exit()

def screen_change(t):
    global screen
    screen = t
    
    if screen == "CREATING_SERVER":
        os.system("../server/server")


process()
