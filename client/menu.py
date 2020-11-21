import pygame, subprocess
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
        self.screen = "MAIN_MENU" #MAIN_MENU, SETTINGS_MENU, CREDITS_SCREEN, CREATING_SERVER, CONNECTING_TO_SERVER
        
        self.RES = RES_LIST[0]
        self.DISPLAY = pygame.display.set_mode(self.RES)

        self.play = True
        self.clicked = False
        self.writing = False

        self.connection = c
        self.server_process = None
        self.error = ""
        self.username = ""


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
            
            Draw.button(self.DISPLAY, "Join Game", x, y, w, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "CONNECTING_TO_SERVER")
            
            y += y/3
            Draw.button(self.DISPLAY, "Host Game", x, y, w, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "CREATING_SERVER")
            
            y += y/3
            Draw.button(self.DISPLAY, "Settings" , x, y, w/2 - 5, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "MAIN_MENU")
            Draw.button(self.DISPLAY, "Credits"  , x + w/2 + 5, y, w/2, h, Colors.GRAY, Colors.DARK_GRAY, Colors.LIGHT_GRAY, self.screen_change, self.clicked, "MAIN_MENU")

            if self.error != "": Draw.draw_text(self.DISPLAY, self.error, 15, [5, self.RES[1]-5], False)

            w, h = self.RES[0]/5, self.RES[1]/20
            Draw.button(self.DISPLAY, self.username, self.RES[0]/2-w/2, self.RES[1]/5, w, h, Colors.WHITE, Colors.WHITE, Colors.BLACK, self.write, self.clicked, [], 1, int(h*3/4))
        
        elif self.screen == "CONNECTING_TO_SERVER":
            Draw.draw_text(self.DISPLAY, "SEARCHING FOR SERVER...", 50, [dims[0]/2, dims[1]/2])
        
        elif self.screen == "CREATING_SERVER":
            Draw.draw_text(self.DISPLAY, "LOADING SERVER...", 50, [dims[0]/2, dims[1]/2])
        
        pygame.display.update()


    def write(self): self.writing = True

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: quit()

            if event.type == pygame.KEYDOWN:
                if self.writing == True:
                    if   event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: self.writing  = False
                    elif event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                    elif event.unicode.isalnum() and len(self.username) <= 10: self.username += event.unicode

                else:
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
                    self.writing = False
                    self.error = ""


    def screen_change(self, t):
        if t == "CREATING_SERVER" or t == "CONNECTING_TO_SERVER":
            if len(self.username) > 5: self.screen = t
            else: self.error = "Username is too short"
        else: self.screen = t
        
        if self.screen == "CREATING_SERVER":
            error = False

            # Create Server
            try: self.server_process = subprocess.Popen("../server/main")
            except Exception as e:
                error = True
                self.error = "Could not Create Server: " + str(e)

            # Connect to Server
            try: self.connection.conn("localhost", 1234)
            except Exception as e:
                error = True
                self.error = "Failed to Connect to Server: " + str(e)

            if not error and self.server_process != None:
                user = bytes(f'{{"username":"{self.username}"}}', 'utf-8')
                self.connection.send(user)

                res = self.connection.recv()
                if res["result"] == "success":
                    self.play = False
                    self.DISPLAY = pygame.display.set_mode(self.RES)
                else: 
                    self.error = "Connection Fail: " + res["result"]
                    self.connection.close()

            self.screen = "MAIN_MENU"
        
        
        if self.screen == "CONNECTING_TO_SERVER":
            error = False

            # Connect to Server
            try: self.connection.conn("localhost", 1234)
            except Exception as e:
                error = True
                self.error = "Failed to Connect to Server: " + str(e)

            if not error:
                user = bytes(f'{{"username":"{self.username}"}}', 'utf-8')
                self.connection.send(user)

                res = self.connection.recv()
                if res["result"] == "success":
                    self.play = False
                    self.DISPLAY = pygame.display.set_mode(self.RES)
                else: 
                    self.error = "Connection Fail: " + res["result"]
                    self.connection.close()

            self.screen = "MAIN_MENU"