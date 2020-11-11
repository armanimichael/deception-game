
import pygame
import math, time, random, sys
from colors import Colors


pygame.init()
pygame.display.set_caption("A Game of Deception")

FPS = 30
RES = [800, 600] # [get_monitors()[0].width, get_monitors()[0].height]

fpsClock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode(RES)#, pygame.FULLSCREEN)


def process():
    while True:
        clicked = False


def draw_grid():
    grid = grid
    size = size
    
    for r in grid:
        for c in r:
            bg = pygame.Rect(0, 0, size, size)
            bg.center = [int(c[0][i]*size + size/2) for i in range(0, 2)]

            pygame.draw.rect(DISPLAY, Colors.BLACK, bg)
            

def draw_UI(num_slots, current):
    w, h = pygame.display.get_surface().get_size()
    bound = w/2 - math.floor(len(p.spell_list)/2) * 50
    
    d = 0
    for i in range(0, num_slot):
        back_color = Colors.DARK_GRAY
        if i == current: edge_color = Colors.YELLOW
        else: edge_color = Colors.BLACK
        
        x, y = [(bound + d*75), h-50]
        skill_slot(50, 50, x, y, back_color, edge_color)
        d += 1

def skill_slot(width, height, x, y, back_color, edge_color, edge=6):
    bg = pygame.Rect(0, 0, width + edge, height + edge)
    bg.center = [x, y]
    pygame.draw.rect(DISPLAY, edge_color, bg)
    
    bg = pygame.Rect(0, 0, width, height)
    bg.center = [x, y]
    pygame.draw.rect(DISPLAY, back_color, bg)
    

def stat_bar(max_width, bar_width, x, y, bar_color, msg="", height=26, back_color=Colors.BLACK, edge=6):        
    bg = pygame.Rect(0, 0, max_width + edge, height + edge)
    bg.midleft = [x - int(edge/2), y]
    pygame.draw.rect(DISPLAY, back_color, bg)
    
    bg = pygame.Rect(0, 0, bar_width, height)
    bg.midleft = [x, y]
    pygame.draw.rect(DISPLAY, bar_color, bg)
    
    draw_text(msg, 15, [x-20, y], bar_color)
    
def button(msg, x, y, w, h, rgb, h_rgb, b_rgb, action=None, args=[], t_dim=20, t_rgb=Colors.BLACK):
    coords = [int(c) for c in (x, y, w, h)]
    color = rgb
    
    if action != None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            color = h_rgb
            if click[0] and action != None and clicked:
                action(args)
    
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
