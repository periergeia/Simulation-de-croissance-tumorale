"""Module contenant les classes :
- Window ;
- SubWindow ;
- ScrollingMenu
pour la gestion des objets modélisant des fenêtres du jeu."""

import math
import random
import pygame
import pygame.freetype
import termcolor
try:
    from constant import COLOR_THEME, COLOR
    from game_objects import Cursor, Layer
    from dev_cell import Cell
    from handle_json import get_value
    from mode import style
except ModuleNotFoundError:
    from module.constant import COLOR_THEME, COLOR
    from module.game_objects import Cursor, Layer
    from module.dev_cell import Cell
    from module.handle_json import get_value
    from module.mode import style


pygame.init()


# ##func_name = {'cell': Cell}


class Window(pygame.sprite.Sprite):

    dict_all = {}
    priority = None

    def __init__(self, name, window):
        """méthode constructrice."""
        self.name = name
        # récupération des données initiales de la sous-fenêtre
        self.data = get_value(file_path=f'./other/style_{style}.json', key=name)
        # ajoute dans le dictionnaire appartenant à la classe, l'object en
        # tant que valeur ayant pour clef son nom `name`
        Window.dict_all[name] = self
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image = pygame.Surface((0, 0))
        self.resize(window)
        self._layer = Layer.find(self)
        pygame.sprite.Sprite.__init__(self, Layer.stock)  # ##

    def resize(self, window):
        """redimenssione selon les valeurs de la fenêtre de jeu `window`, une
        instance de pygame.Surface."""
        main_window_w, main_window_h = window.get_width(), window.get_height()
        x_value = round(self.data['relative']['x'] * main_window_w)
        y_value = round(self.data['relative']['y'] * main_window_h)
        w_value = round(self.data['relative']['w'] * main_window_w)
        h_value = round(self.data['relative']['h'] * main_window_h)
        self.rect.update(x_value, y_value, w_value, h_value)
        self.create_surface()

    def create_surface(self):
        """instance permettant de redéfinir l'attribut image de l'instance
        avec les valeurs changées de l'attribut rect."""
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(COLOR[COLOR_THEME[self.data['color']]['background']])


class SubWindow(pygame.sprite.OrderedUpdates):

    border_width = 0
    group = {}

    def __init__(self, name, window):
        pygame.sprite.OrderedUpdates.__init__(self)
        SubWindow.group[name] = self
        self.display = SubWindow.Display(name, window)
        self.button = SubWindow.Button(self.display)
        # self.add(SubWindow.Display(name, window), SubWindow.Button)
        self.add(self.button)
        Layer.all_sprites.add(self)

    @staticmethod
    def characteristics_size_change(window):
        """définition du rayon d'un bouton de fermeture selon les dimensions
        de la fenêtre ainsi que la taille des bordures selon `window` un
        objet pygame.Surface correspondant aux dimensions de la fenêtre de
        jeu pygame. Ces deux dimensions sont stockés dans les attributs de
        classe leur correspondant."""
        # définition de la taille du bouton de fermeture
        SubWindow.Button.radius = round(math.sqrt(window.get_width() / 50 + window.get_height() / 50))
        # définition de l'objet pygame.Surface correspondant à l'image du bouton
        SubWindow.Button.image = pygame.Surface((SubWindow.Button.radius * 2, SubWindow.Button.radius * 2))
        SubWindow.Button.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(SubWindow.Button.image,
                           COLOR[COLOR_THEME[Window.dict_all['sub_window_1'].data['color']]['background']],
                           SubWindow.Button.image.get_rect().center,
                           SubWindow.Button.radius)
        pygame.draw.circle(SubWindow.Button.image,
                           COLOR[COLOR_THEME[Window.dict_all['sub_window_1'].data['color']]['border']],
                           SubWindow.Button.image.get_rect().center,
                           SubWindow.Button.radius, 1)
        # définition de l'objet pygame.mask.Mask associé
        SubWindow.Button.mask = pygame.mask.from_surface(SubWindow.Button.image)

        # définition du nombre de pixel pour l'épaisseur des bordures
        SubWindow.border_width = round(math.sqrt(window.get_width() / 250 + window.get_height() / 250))
        # SubWindow.border_width = round(math.sqrt(window.get_width() / 205 + window.get_height() / 114))
        print("bordure taille", SubWindow.border_width)  # ##

    @staticmethod
    def change_visibility(name):
        try:
            Layer.all_sprites.remove(SubWindow.group[name])
        except KeyError:  # ## voir à changer
            pass


    class Button(pygame.sprite.Sprite):

        radius = 0
        image = None
        mask = None

        def __init__(self, window_display):

            self.name = window_display.name  # ##
            self.rect = pygame.Rect(0, 0, 0, 0)  # ## moyen d'enlever
            self.parent = window_display
            self._layer = window_display._layer
            pygame.sprite.Sprite.__init__(self)

        def resize(self):  # ##
            self.image = SubWindow.Button.image
            self.mask = SubWindow.Button.mask
            self.rect = self.image.get_rect(center=(self.parent.rect.x + self.parent.rect.w - 1.5 * SubWindow.Button.radius, self.parent.rect.y + 1.5 * SubWindow.Button.radius))


    class Border(pygame.sprite.Group):

        def __init__(self, window_display):
            pygame.sprite.Group.__init__(self)
            self.parent = window_display
            self.stock = {}
            layer = window_display._layer
            for edge in [str(i) for i in range(4)]:
                self.stock[edge] = SubWindow.Border.Edge(edge, window_display.name, layer)
                self.add(self.stock[edge])

        def resize(self):
            # 0 --> bord du haut (top)
            self.stock['0'].rect.update(self.parent.rect.x,
                                        self.parent.rect.y,
                                        self.parent.rect.w,
                                        SubWindow.border_width)
            # 1 --> bord du bas (bottom)
            self.stock['1'].rect.update(self.parent.rect.x,
                                        self.parent.rect.h + self.parent.rect.y - SubWindow.border_width,
                                        self.parent.rect.w,
                                        SubWindow.border_width)
            # 2 --> bord de gauche (left)
            self.stock['2'].rect.update(self.parent.rect.x,
                                        self.parent.rect.y,
                                        SubWindow.border_width,
                                        self.parent.rect.h)
            # 3 --> bord de droite (right)
            self.stock['3'].rect.update(self.parent.rect.x + self.parent.rect.w - SubWindow.border_width,
                                        self.parent.rect.y,
                                        SubWindow.border_width,
                                        self.parent.rect.h)
            self.update_image()

        def update_image(self):
            for sprite in self:
                sprite.image = pygame.Surface(sprite.rect.size)
                sprite.image.fill(COLOR_THEME[self.parent.data['color']]['border'])


        class Edge(pygame.sprite.Sprite):  # ## too few public method (0/2)
            """
            0 : top,
            1 : bottom,
            2 : left,
            3 : right"""

            # essayer de faire hériter d'une instance et non d'une classe
            def __init__(self, number, name, layer):
                self.number = number
                self.name = name
                self._layer = layer
                self.rect = pygame.Rect(0, 0, 0, 0)
                pygame.sprite.Sprite.__init__(self)


    class Display(Window):

        def __init__(self, name, window, func=None):
            super().__init__(name, window)
            # définition des bords de l'affichage de la sous-fenêtre
            self.borders = SubWindow.Border(self)
            SubWindow.group[self.name].add(self, self.borders)  # ##
            # self.func = Cell(random.randint(5, 15), self.image)

        def test_side(self, cursor):
            """fonction permettant de vérifier la position du curseur sur la
            sous-fenêtre, elle change le curseur en fonction de cette position,
            optant pour un curseur de redimensionnement correspondant au bord sur
            lequel se situe le curseur.
            `cursor` est une instance de la classe Cursor."""
            def set_changes(collided):
                """fonction cherchant le curseur adéquat selon les bords de la
                sous-fenêtre en collision avec le curseur. `collided` est une liste
                contenant les sprites en collision."""
                # mis à jour du/des bord(s) à tester
                Cursor.test = collided
                # il s'agit de récupérer le nom des sprites concernés
                # par une collision avec le curseur
                collided = list((map(lambda x : x.number, collided)))
                # dans le cas où il n'y en a pas
                if not collided:
                    Cursor.set_current('default')
                # si il y a exactement un sprite entré en collision
                elif len(collided) == 1:
                    # dans le cas où il s'agit de top ou bottom
                    if int(collided[0]) < 2:
                        Cursor.set_current('NS')
                    # autrement, il ne peut que s'agir de right ou left
                    else:
                        Cursor.set_current('WE')
                # deux sprites sont en collision, il reste à déterminer lesquels
                else:
                    # attribution d'une valeur à l'intersection de sprites, selon
                    # leur nom pour evaluer l'angle de la sous-fenêtre qui est
                    # sous le curseur
                    value = int(''.join(collided))
                    # value vaut 3 ou 12, il s'agit donc des angles haut-droit ou
                    # bas-gauche
                    if value % 3 == 0:
                        Cursor.set_current('NESW')
                    # il ne peut alors s'agir que des angles restants, à savoir :
                    # haut-gauche ou bas-droit
                    else:
                        Cursor.set_current('NWSE')

            def check_edge(collided):
                """vérifie si la souris est toujours sur le sprite de bord stocké
                en mémoire, si non, on appelle la fonction de recherche pour mettre
                à jour la variable et l'apparence du curseur.
                `collided` est une liste contenant les sprites en collision."""
                # tester le nombre de sprites entré en collision est suffisant
                nb_collided = len(pygame.sprite.groupcollide(collided, Cursor.test, False, False))
                if nb_collided != len(Cursor.test):
                    set_changes(collided)

            def check_no_collision(collided):
                """vérifie si une collision avec un sprite de bord a lieu.
                `collided` est une liste contenant les sprites en collision."""
                # dans le cas où la souris est bien en collision avec au moins un élément
                if collided:
                    set_changes(collided)

            # création d'une liste des bords touchée
            collided = pygame.sprite.spritecollide(cursor, self.borders, False)
            if Cursor.test:
                check_edge(collided)
            else:
                check_no_collision(collided)


class ScrollingMenu(pygame.sprite.OrderedUpdates):
    """modélise un bouton permettant d'afficher au survol de la souris des
    options d'affichage ou autres. Chaque option est graphiquement défini
    comme une ligne contenant dans l'ordre : image (optionnelle), label, signe
    (correspondant à un signe de validation, pas toujours apparent, dépend des
    choix du joueur).

    ATTRIBUTS:
    - `content` (list) ;
    - `number` (int) ;
    - `` () ;
    - `` () ;
    - `` () ;
    """
    count = 0
    font_size = None

    def __init__(self, name, menu_names, window):
        """méthode constructrice de la classe prenant en argument :
        `name` est une chaîne de caractères pour attribuer un nom au menu
        déroulant, `menu_names` une liste de chaînes de caractères et
        `window` l'objet pygame.Surface de la fenêtre de jeu pygame."""
        pygame.sprite.OrderedUpdates.__init__(self)
        self.content = menu_names
        self.displayed = False

        m = ScrollingMenu.Menu(name)
        
        self.add(m)
        self.add(Text(name, m, 2/3))

        for name in menu_names:
            SubWindow(name, window)
        self.name = name
        Layer.all_sprites.add(self)


    class Menu(pygame.sprite.Sprite):

        def __init__(self, name):
            self.number = ScrollingMenu.count
            ScrollingMenu.count += 1
            self.name = name
            self._layer = 0 # le dernier
            pygame.sprite.Sprite.__init__(self)

        def resize(self, window):
            main_window_w, main_window_h = window.get_width(), window.get_height()
            x_value = round(self.number * 0.1 * main_window_w)
            w_value = round(0.1 * main_window_w)
            h_value = round(0.05 * main_window_h)
            self.rect = pygame.Rect(x_value, 0, w_value, h_value)
            self.image = pygame.Surface(self.rect.size)
            self.image.fill((0, 150, 0))

    def create_text(self):
        ...


    def create_surface(self):
        """"""
        """self.surface = pygame.Surface()
        font_height = 0.05 * WINDOW_DATA['height']
        font = pygame.font.Font("others/Anton-Regular.ttf",
                                     get_font_size(font_height))"""


    def display(self, surface):
        surface.blit(self.surface, self.get_position())


class Text(pygame.sprite.Sprite):

    font = {}
    for number, size in {i : i * 3 + 6 for i in range(5)}.items():
        font[number] = {}
        font[number]['font'] = pygame.font.Font("other/Anton-Regular.ttf", size)
        font[number]['height'] = font[number]['font'].size('.')[1]

    def __init__(self, content, sprite, height_ratio):
        """`content` str, `surface` pygame.Surface, area_ratio (0:1)"""
        self.content = content
        self.parent = sprite
        self.name = sprite.name
        self.height_ratio = height_ratio
        self._layer = sprite._layer
        pygame.sprite.Sprite.__init__(self)

    @staticmethod
    def find_size():
        ...

    def resize(self, a):  # ## :/
        """récupère une valeur de taille de police selon `font_height` un entier
        naturel représentant la hauteur de font voulu en nombre de pixel sur la
        fenêtre de jeu."""  # ##
        area_width, area_height = self.parent.rect.size
        font_height = area_height * self.height_ratio
        print(font_height)
        # détermination de la hauteur max du text
        if font_height > Text.font[0]['height']:
            font_size = 0
        else:
            font_size = 0
            try:
                while font_height >= Text.font[font_size]['height']:
                    font_size += 1
            except IndexError:
                pass
        try:
            while Text.font[font_size]['font'].size(self.content)[0] > area_width:
                font_size -= 1
        except:
            pass
        self.image = Text.font[font_size]['font'].render(self.content, 1, (150, 0, 0))
        self.rect = self.image.get_rect(center=self.parent.rect.center)
        print("taille de font :  ", font_size)
