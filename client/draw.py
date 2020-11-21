
import pygame, math

class Draw:
    def button(self, surface, msg, x, y, w, h, rgb, h_rgb, b_rgb, action=None, clicked=False, args=[], border=3, t_dim=20, t_rgb=(0,0,0)):
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
        
        pygame.draw.rect(surface, color, coords)
        pygame.draw.rect(surface, b_rgb, coords, border)
        
        self.draw_text(surface, msg, t_dim, (int(x + (w/2)), int(y + (h/2))))

    def draw_text(self, surface, msg, h, coords, centered=True, color=(0,0,0)):
        font = pygame.font.Font("freesansbold.ttf", h)
        textSurf = font.render(msg, True, color)
        textRect = textSurf.get_rect()

        if centered: textRect.center = [int(c) for c in coords]
        else       : textRect.bottomleft = [int(c) for c in coords]

        surface.blit(textSurf, textRect)

    def drawRegularPolygon(self, surface, color, numSides, tiltAngle, x, y, radius):
        pts = []
        for i in range(numSides):
            x = x + radius * math.cos(tiltAngle + math.pi * 2 * i / numSides)
            y = y + radius * math.sin(tiltAngle + math.pi * 2 * i / numSides)
            pts.append([int(x), int(y)])
        pygame.draw.polygon(surface, color, pts)

DrawHandler = Draw()
