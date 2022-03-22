import pygame
import pygame.freetype
import sys
try:
    from constant import WINDOWS
    from windows import SubWindow
except ModuleNotFoundError:
    from module.constant import WINDOWS
    from module.windows import SubWindow


class Game:

    def __init__(self):
        # définition de variables de fenêtre
        FULLSCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][1]
        WINDOW_HEIGHT = round(FULLSCREEN_WIDTH * 2/3)
        WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8)
        WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # définition de la fenêtre pygame de taille dynamique
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.state = 1
        # importation d'image
        icon = pygame.image.load("./image/logo.ico").convert_alpha()
        # personnalisation de la fenêtre
        pygame.display.set_caption("Simulation de la croissance de cellules tumorales")
        pygame.display.set_icon(icon)
    
    def resize(self):
        SubWindow.button_size_change(self.screen)
        for sprite in self.subwindows:
            sprite.resize(self.screen)
    
    def run(self):
        self.subwindows = pygame.sprite.Group()
        for name in WINDOWS:
            self.subwindows.add(SubWindow(name, self.screen))
        
        clock = pygame.time.Clock()
        while self.state:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    pass
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.resize()
            
            self.subwindows.draw(self.screen)
            clock.tick(60)
            pygame.display.set_caption(f'FPS: {clock.get_fps()}')
            pygame.display.update()
            