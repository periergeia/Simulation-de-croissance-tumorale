"""module contenant la classe Game pour la gestion du gameplay."""


# importation de modules
import sys
import pygame
import pygame.freetype
try:
    from constant import FUNCTION, SUBWINDOWS_NAMES, FUNCTIONNALITIES
    from game_objects import Cursor, Layer
    from windows import Image, Graphical, Window, SubWindow, ScrollingMenu
except ModuleNotFoundError:
    from module.constant import FUNCTION, SUBWINDOWS_NAMES, FUNCTIONNALITIES
    from module.game_objects import Cursor, Layer
    from module.windows import Image, Graphical, Window, SubWindow, ScrollingMenu


# menu permettant de choisir une mutation, qui apparait selon une
# certaine proba ou une clock particulière
# ajouter sprite pour définir espace pour grab
# ________changement bonhomme, avec, sans organe dans nouveau menu
# ___subwindow visible au début ?

# ##
# pylint: disable=E1101

class Game:
    """Classe gérant le gameplay.

    ATTRIBUTS DE CLASSE:
    - `PRIORITY_CHANGE` (int) : est un user event pour relever les changements
    de priorité de sprite, le plus haut placé selon les calque et où le curseur
    se situe ;
    - `RESIZING` (int) : est un user event pour le changement de dimension
    d'une sous-fenêtre.

    ATTRIBUTS:
    - `check_priority_change` (bool) ;
    - `cursor` (Cursor) : instance sprite pour gérer les données du curseur
    dans le jeu ;
    - `resizing` (dict) : contient différentes aleurs décrit ci-dessous :
        - 'can_resize' (bool) : indique s'il est possible de redimensionner,
        - 'is_resizing' (bool) : état du redimensionnement d'une sous-fenêtre,
        - 'side'(None | str) : stocke le nom du curseur à prendre lors du
        redimensionnement d'une sous-fenêtre,
        - 'window'(None | SubWindow): stocke la fenêtre devant être
        redimensionnée ;
    - `screen` (pygame.Surface) : il s'agit de l'instance pygame.Surface
    associé à la fenêtre de jeu ;
    - `state` (int) : définit le stade du jeu, tant qu'il vaut 1, la
    simulation continue, 0, si elle doit se terminer."""

    PRIORITY_CHANGE = pygame.USEREVENT + 1
    RESIZING = pygame.USEREVENT + 2

    def __init__(self):
        """méthode constructrice dans laquelle est définie les
        caractéristiques de la fenêtre de jeu."""
        # définition de variables de fenêtre
        fullscreen_width = pygame.display.get_desktop_sizes()[0][1]
        window_height = round(fullscreen_width * 2/3)
        window_width = round(window_height * 1.8)
        window_size = (window_width, window_height)
        print(window_size)
        # définition de la fenêtre pygame de taille dynamique
        self.screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        self.state = 1
        self.cursor = Cursor()
        self.check_priority_change = pygame.mouse.get_focused()
        self.resizing = {'can_resize': False,
                         'is_resizing': False,
                         'side': None,
                         'window': None}

        # importation d'image
        icon = pygame.image.load("./image/logo.ico").convert_alpha()  # ##déplacement ?
        # personnalisation de la fenêtre
        pygame.display.set_caption("Simulation de la \
                                   croissance de cellules tumorales")
        pygame.display.set_icon(icon)

    @staticmethod
    def static_mouse_event():
        """renvoie un booléen, True si le sprite prioritaire se trouve
        changé, False sinon, dans le cas où il est différent du précédent,
        un user event est généré et est envoyé dans la queue des évènements
        pygame."""
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

    def resize(self):
        """méthode appelant les méthodes de redimensionnement propre à chaque
        instance de sprites apparent."""
        # changement de taille des caractéristiques générales aux objets
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
                if isinstance(sprite, SubWindow.Display):
                    sprite.resize(self.screen)
                    SubWindow.group[sprite.name].button.resize()
                    sprite.borders.resize()
        ScrollingMenu.resize(self.screen)

    def check_event(self, event):
        """`event` est un objet pygame.event, dans la méthode, il s'agit de
        gérer les évènements dépendant d'actions de l'utilisateur avec la
        souris notamment."""
        # le bouton pour quitter de la fenêtre de jeu est cliqué
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # la fenêtre de jeu est redimensionnée par l'utilisateur
        if event.type == pygame.VIDEORESIZE:
            self.resize()
        # gestion des actions liés aux différents type d'objets de jeu
        self.handle_window_priority(event)
        self.handle_subwindow_changes(event)
        self.handle_scrolling_menu(event)

        if event.type == pygame.KEYDOWN:  # ##
            if event.key == pygame.K_c:
                Layer.test()

    def handle_window_priority(self, event):
        """ensemble d'actions selon `event`, objet pygame.event, gérant la
        priorité sur une sous-fenêtre."""
        # pour des raisons d'économie de performances :
        # lorsque le curseur est sort de la fenêtre de jeu pygame
        if event.type == pygame.WINDOWLEAVE:
            # on ne vérifie plus s'il y a une priorité sur une sous-fenêtre
            self.check_priority_change = False
            # le redimensionnement n'est plus permis
            self.resizing['can_resize'] = False
            self.resizing['is_resizing'] = False

        # si le curseur entre dans la fenêtre de jeu pygame
        if event.type == pygame.WINDOWENTER:
            # on permet de nouveau les vérification liées à la priorité
            self.check_priority_change = True
        # ##
        if event.type == Game.PRIORITY_CHANGE:
            print('-----', Window.priority)

    def handle_subwindow_changes(self, event):
        """ensemble d'actions selon `event`, objet pygame.event,
        gérant les sous-fenêtres."""
        # un clic de la souris s'opère
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)  # ##
            # on vérifie si un bouton de fermeture de sous-fenêtre est cliqué
            try:
                button = SubWindow.group[Window.priority].button
                if pygame.sprite.collide_mask(self.cursor, button):
                    SubWindow.change_visibility(Window.priority)
                    Layer.test()
            # dans le cas où Window.priority est de type Nonetype
            except AttributeError:  # ## :/
                print(Window.priority)
            # lorsque le nom de la sous-fenêtre n'est pas celui d'un nom d'une
            # instance de sous-fenêtre
            except KeyError:
                pass
            # permet de maintenir la possibilité de redimensionner une
            # sous-fenêtre
            if self.resizing['can_resize']:
                self.resizing['is_resizing'] = True
                self.check_priority_change = False

        # user event : une sous-fenêtre peut être redimensionnée
        if event.type == Game.RESIZING:
            try:
                self.resizing['window'] = Window.dict_all[Window.priority]
            except KeyError:
                pass
            self.resizing['can_resize'] = event.state
            self.resizing['side'] = event.side

        # lorsque le curseur est en mouvement
        if event.type == pygame.MOUSEMOTION:
            # si une sous-fenêtre est sur le point d'être redimensionnée
            if self.resizing['is_resizing']:
                # on essaie de redimensionner la sous-fenêtre en fonction
                try:
                    subwindow_to_resize = self.resizing['window'].parent
                    Layer.move_to_top(subwindow_to_resize)
                    subwindow_to_resize.single_resize(self.screen)
                    Cursor.set_current(self.resizing['side'])
                except AttributeError:
                    pass

        # lorsque le bouton de la souris est relâché
        if event.type == pygame.MOUSEBUTTONUP:
            # si une sous-fenêtre est sur le point d'être redimensionnée
            if self.resizing['is_resizing']:
                # changement des valeurs de booléens nécéssaires
                #try:
                self.resizing['can_resize'] = False
                self.resizing['is_resizing'] = False
                self.check_priority_change = True
                # ##except AttributeError:
                    #pass

    def handle_scrolling_menu(self, event):
        """ensemble d'actions selon `event`, objet pygame.event, gérant
        les menus déroulant."""
        # si la souris est cliquée
        if event.type == pygame.MOUSEBUTTONDOWN:
            # dans le cas où une collision s'opère entre le curseur et
            # un menu déroulant
            scrolling_menu_collide = pygame.sprite.spritecollide(
                                        self.cursor,
                                        Layer.scrolling_menus, False)
            if scrolling_menu_collide:
                # la visibilité du menu_déroulant est changée
                scrolling_menu_collide[0].parent.change_visibility()
            # vérification si une option de menu est cliqué
            menu_options_collide = pygame.sprite.spritecollide(
                                        self.cursor,
                                        Layer.menu_options, False)
            if menu_options_collide:
                # la visibilité du menu_déroulant est changée
                try:
                    if isinstance(SubWindow.group[menu_options_collide[0].name].display.func, Graphical):
                        print('>>>>>>>>>>>>', menu_options_collide[0].name)
                        SubWindow.change_visibility(menu_options_collide[0].name)
                except KeyError:
                    print('>>>>>>>>>>>>', menu_options_collide[0].name)
                    FUNCTION[menu_options_collide[0].name]()

    def run(self):
        """boucle principale de jeu."""
        Window('space', self.screen)
        Image("./image/vue_organe.png", 'space', (0.31, 0.15, 0.2, 0.8), 'organe')
        Image("./image/vue_sans_organe.png", 'space', (0.31, 0.15, 0.2, 0.8), 'sans_organe')
        ScrollingMenu('ORGANES', SUBWINDOWS_NAMES, self.screen, 1)
        ScrollingMenu('OPTIONS', FUNCTIONNALITIES, self.screen, 2)
        """ScrollingMenu('■ ■ ■', [f'sub_window_{i}' for i in range(1, 3)], self.screen)
        ScrollingMenu('■ ■', ['sub_window_3'], self.screen)
        ScrollingMenu('■', ['sub_window_4'], self.screen)"""
        # Image("./image/vue_organe.png", 'space', (0.31, 0.15, 0.2, 0.8))

        # met à jour les dimensions de chaque objet du jeu
        self.resize()
        Layer.all_sprites.add(Layer.scrolling_menus)
        # permet de filtrer sur les évènements pygame d'un objet pygame.Event
        # pygame.event.set_blocked(pygame.MOUSEMOTION)
        # pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        clock = pygame.time.Clock()
        self.resizing['can_resize'] = Cursor.get_resizing_status()

        while self.state:
            for event in pygame.event.get():  # ## ici ou dans check event ?
                self.check_event(event)

            if self.check_priority_change:
                self.static_mouse_event()
                try:
                    SubWindow.group[Window.priority].display.test_side(self.cursor)
                # dans le cas où il s'agit d'un objet Window
                except KeyError:
                    Cursor.set_current('default')

            # remplissage du fond en gris
            self.screen.fill((40, 40, 40))
            # dessin de tous les sprites ordonnés par calques
            Layer.all_sprites.draw(self.screen)
            # mise à jour des sprites
            pygame.display.update()
            # mise à jour de la position de la souris
            self.cursor.update()

            pygame.display.set_caption(f'Simulation de la croissance de cellules tumorales \
                                       FPS: {clock.get_fps()}')
            clock.tick(60)
