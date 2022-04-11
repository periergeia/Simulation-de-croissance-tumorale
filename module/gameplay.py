"""module contenant la classe Game pour la gestion de la gameplay."""

import random
import sys
import pygame
import pygame.freetype
try:
    from constant import SUBWINDOWS_NAMES
    from game_objects import Cursor, Layer
    from useful import Chronometer
    from windows import Window, SubWindow, ScrollingMenu
except ModuleNotFoundError:
    from module.constant import SUBWINDOWS_NAMES
    from module.game_objects import Cursor, Layer
    from module.useful import Chronometer
    from module.windows import Window, SubWindow, ScrollingMenu


# Window priority avec name et non pas le sprite ?


class Game:
    """Classe gérant la gameplay.
    
    ATTRIBUTS:
    - `screen` () ;
    - `state` () ;
    - `cursor` () ;
    - `` () ;
    - `` () ;
    """
    PRIORITY_CHANGE = pygame.USEREVENT + 1
    RESIZING = pygame.USEREVENT + 2

    def __init__(self):
        """méthode constructrice dans laquelle est définie les
        caractéristiques de la fenêtre de jeu."""
        # définition de variables de fenêtre
        FULLSCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][1]
        WINDOW_HEIGHT = round(FULLSCREEN_WIDTH * 2/3)
        WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8)
        WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
        # définition de la fenêtre pygame de taille dynamique
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.state = 1
        self.cursor = None  # ## ?
        self.can_resize = False
        
        # importation d'image
        icon = pygame.image.load("./image/logo.ico").convert_alpha()  # ##déplacement ?
        # personnalisation de la fenêtre
        pygame.display.set_caption("Simulation de la croissance de cellules tumorales")
        pygame.display.set_icon(icon)
    
    def resize(self):
        """méthode appelant les méthodes de redimensionnement propre à chaque
        instance de sprites apparent."""
        # changement de tailles des caractéristiques générales aux objets
        # SubWindow à savoir l'épaisseur des bordures et le rayon d'un bouton
        SubWindow.characteristics_size_change(self.screen)
        # redimensionnement de tous les éléments se situant sur le calque le
        # plus bas contenant les sprites des menus déroulant et l'objet Window
        for sprite in Layer.all_sprites.get_sprites_from_layer(0):
            sprite.resize(self.screen)
        # redimenssionement de tous les sprites de sous-fenêtre apparents sur
        # le sprite de l'instance Window
        for index in Layer.all_sprites.layers()[1:]:
            for sprite in Layer.all_sprites.get_sprites_from_layer(index):
                if type(sprite) == SubWindow.Display:
                    sprite.resize(self.screen)
                    SubWindow.group[sprite.name].button.resize()
                    sprite.borders.resize()        
    
    def static_mouse_event(self):
        # vérifie si la souris est sur la fenêtre "prioritaire"
        if Window.priority == Layer.mouse_over():
            return True
        # dans le cas où la souris n'est pas sur la fenêtre
        # redéfinition d'une fenêtre prioritaire

        Window.priority = Layer.mouse_over()
        # si la nouvelle fenêtre prioritaire est bien sur la fenêtre pygame
        if Window.priority is not None:  # ## condition inutile ?, :/ changer
            # envoi de l'évènement PRIORITY_CHANGE
            pygame.event.post(pygame.event.Event(Game.PRIORITY_CHANGE))
            return True
        return False
    
    def check_event(self, event):
        """event est un objet pygame.event """
        ...
    
    def run(self):
        
        Layer.all_sprites.add(Window('space', self.screen))
        ScrollingMenu("test lambda", SUBWINDOWS_NAMES, self.screen)
        Layer.test()

        cursor = Cursor()  # ## en faire un attribut de la classe Game ?

        self.resize()
        # permet de filtrer sur les évènements pygame d'un objet pygame.Event
        # pygame.event.set_blocked(pygame.MOUSEMOTION)
        # pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        clock = pygame.time.Clock()
        check_priority_change = pygame.mouse.get_focused()
        while self.state:
            
            for event in pygame.event.get():
                # print(timer.get_chrono_value())
                #print(event)
                #print()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.WINDOWLEAVE:
                    check_priority_change = False
                if event.type == pygame.WINDOWENTER:
                    check_priority_change = True

                if event.type == Game.PRIORITY_CHANGE:
                    #Window.priority = event.dict['rect']['over']
                    #SubWindow.dict_all['sub_window_2'].update()
                    print('-----', Window.priority)

                if Cursor.resizing:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        ...
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                     #if pygame.sprite.collide_mask(cursor, Window.priority):
                    # if pygame.sprite.collide_mask(cursor, SubWindow.button_mask):
                    # if cursor.mask.overlap(SubWindow.button_mask, offset):
                    #if SubWindow.button_mask
                    try:
                        # if SubWindow.group[Window.priority].button.rect.collidepoint(pygame.mouse.get_pos()):
                        if pygame.sprite.collide_mask(cursor, SubWindow.group[Window.priority].button):
                            SubWindow.change_visibility(Window.priority)
                            Layer.test()
                    # dans le cas où Window.priority est de type Nonetype
                    except AttributeError:  # ## :/
                        print(Window.priority)
                    except KeyError:
                        pass
                if event.type == pygame.VIDEORESIZE:
                    self.resize()
            
            if check_priority_change:
                self.static_mouse_event()
                try:
                    SubWindow.group[Window.priority].display.test_side(cursor)
                # dans le cas où il s'agit d'un objet Window
                except KeyError:
                    Cursor.set_current('default')  # ##
                except AttributeError:
                    Cursor.set_current('default')  # ## pas de name pour menuderoulant moment

            # dessin de tous les sprites ordonnés par calques
            Layer.all_sprites.draw(self.screen)
            # mise à jour des sprites
            pygame.display.update()
            # mise à jour de la position de la souris
            cursor.update()

            pygame.display.set_caption(f'FPS: {clock.get_fps()}')  # ##
            clock.tick(60)
            
