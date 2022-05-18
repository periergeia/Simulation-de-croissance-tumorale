"""Module contenant les classes :
- Window ;
- SubWindow ;
- ScrollingMenu
pour la gestion des objets modélisant des fenêtres du jeu."""


import math
import pygame
try:
    from constant import COLOR_THEME, COLOR
    from game_objects import Cursor, Layer
    from handle_json import get_value
    from mode import style
    from useful import get_top_left_pos, Text
except ModuleNotFoundError:
    from module.constant import COLOR_THEME, COLOR
    from module.game_objects import Cursor, Layer
    from module.handle_json import get_value
    from module.mode import style
    from module.useful import get_top_left_pos, Text


pygame.init()


class Window(pygame.sprite.Sprite):
    """modélise une 'fenêtre' à savoir une surface dans la fenêtre de jeu
    pygame laquelle est sensible aux changements de dimension de cette
    dernière.

    ATTRIBUTS DE CLASSE:
    - `dict_all` (dict) : contient toutes les références d'instance créée
    avec la classe repertoriées par le nom en tant que clef du
    dictionnaire ;
    - `priority` (None | str) : correspond au nom de la fenêtre sur laquelle
    le curseur se situe.

    ATTRIBUTS:
    - `data` (dict) : contient les données (position relative,
    taille relative, ...) de l'objet fenêtre récupérées dans un fichier JSON
    (précisé par le nom de la fenêtre) ;
    - `image` (pygame.Surface) : représentation graphique de l'instance ;
    - `_layer` (int) : position du calque ;
    - `name` (str) : nom de la fenêtre ;
    - `rect` (pygame.Rect) : défini la position et les dimensions utiles à
    l'affichage."""

    dict_all = {}
    priority = None

    def __init__(self, name, window):
        """méthode constructrice."""
        self.name = name
        # récupération des données initiales de la fenêtre
        self.data = get_value(file_path=f'./other/style_{style}.json', key=name)
        # ajoute dans le dictionnaire appartenant à la classe, l'object en
        # tant que valeur ayant pour clef son nom `name`
        Window.dict_all[name] = self
        # quelques formalités pour pylint
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
    """modélise une 'sous-fenêtre' une surface pouvant être redimensionnée,
    supprimée de la fenêtre de jeu grâce à un bouton situé dans le coin
    haut-droit de sa surface rectangulaire.

    ATTRIBUTS DE CLASSE:
    - `border_width` (int) : correpond à l'épaisseur en pixel de la bordure
    d'une sous-fenêtre ;
    - `group` (dict) : contient les instances de la classe, les clefs étant
    les noms des sous-fenêtres.

    ATTRIBUTS:
    - `button` (SubWindow.Button) : bouton de la sous-fenêtre ;
    - `display` (SubWindow.Button) : écran de la sous-fenêtre.

    ARCHITECTURE DE LA CLASSE:
    SubWindow
        |___Button
        |___Border
            |___Edge
        |___Display
    """

    border_width = 0
    group = {}

    def __init__(self, name, window):
        """méthode constructrice."""
        pygame.sprite.OrderedUpdates.__init__(self)
        SubWindow.group[name] = self
        self.display = SubWindow.Display(name, window, self)
        self.button = SubWindow.Button(self.display)
        self.add(self.button)
        # l'instance est ajoutée à Layer.all_sprites afin d'être rendu visible
        Layer.all_sprites.add(self)

    @staticmethod
    def characteristics_size_change(window):
        """définition du rayon d'un bouton de fermeture selon les dimensions
        de la fenêtre ainsi que la taille des bordures selon `window` un
        objet pygame.Surface correspondant aux dimensions de la fenêtre de
        jeu pygame. Ces deux dimensions sont stockés dans les attributs de
        classe leur correspondant."""
        # définition de la taille du bouton de fermeture
        SubWindow.Button.radius = round(math.sqrt(window.get_width() / 50 + \
                                                  window.get_height() / 50))
        # définition de l'objet pygame.Surface pour l'image du bouton
        SubWindow.Button.image = pygame.Surface((SubWindow.Button.radius * 2,
                                                 SubWindow.Button.radius * 2))
        SubWindow.Button.image.set_colorkey((0, 0, 0))
        color_theme = COLOR_THEME[Window.dict_all['sub_window_1'].data['color']]
        pygame.draw.circle(SubWindow.Button.image,
                           COLOR[color_theme['background']],
                           SubWindow.Button.image.get_rect().center,
                           SubWindow.Button.radius)
        pygame.draw.circle(SubWindow.Button.image,
                           COLOR[color_theme['border']],
                           SubWindow.Button.image.get_rect().center,
                           SubWindow.Button.radius, 1)
        # définition de l'objet pygame.mask.Mask associé
        SubWindow.Button.mask = pygame.mask.from_surface(SubWindow.Button.image)

        # définition du nombre de pixel pour l'épaisseur des bordures
        SubWindow.border_width = round(math.sqrt(window.get_width() / 250 + \
                                                 window.get_height() / 250))
        print("bordure taille", SubWindow.border_width)  # ##

    @staticmethod
    def change_visibility(name):
        try:
            Layer.all_sprites.remove(SubWindow.group[name])
        except KeyError:  # ## voir à changer
            pass

    def resize(self, window):
        """méthode appelant les méthodes de redimensionnement propre à chaque
        instance de sprites de la classe."""
        # redimenssionement de tous les sprites de sous-fenêtre apparents sur
        # le sprite de l'instance Window
        self.button.resize()
        self.display.resize(window)
        self.display.borders.resize()

    def single_resize(self, window):
        """fonction astucieuse pour le redimensionnement d'une sous-fenêtre."""
        value = {'0': ('y', 'h'),
                 '1': ('h', 'y'),
                 '2': ('x', 'w'),
                 '3': ('w', 'x')}  # ##déplacer ?
        # pour chaque bord en contact avec le curseur (deux au plus)         
        for edge in Cursor.wall:
            # previous_relative_value peut être inutilisé dans certains cas
            # il est plus rentable que de vérifier si edge = 0 | edge = 2
            previous_relative_value = self.display.data['relative'][value[edge][0]]
            # il s'agit de savoir si les valleurs changer sont dépendant de la
            # largeur ou de la longueur de la fenêtre de jeu, on rappelle que
            # tout est défini relativement à celle-ci en terme de
            # proportionnalité, x et w dépendent de la largeur tandis que y et
            # h sont selon la hauteur
            size_index = 1 if int(edge) < 2 else 0
            # changement d'une valeur qui prend en considération la position
            # de la souris et du bord
            self.display.data['relative'][value[edge][0]] = pygame.mouse.get_pos()[size_index] / window.get_size()[size_index]
            # s'il s'agit du bord haut ('0') ou du bord gauche ('2')
            if int(edge) % 2 == 0:
                # il s'agit de changer la hauteur (si bord haut)
                # (respectivement la largeur (si bord gauche)) afin de donner
                # l'illusion que la position du bord bas (respectivement bord
                # droit) reste inchangée
                diff = self.display.data['relative'][value[edge][0]] - previous_relative_value
                self.display.data['relative'][value[edge][1]] = self.display.data['relative'][value[edge][1]] - diff
            # il ne peut que s'agir du bord bas ('1') ou du bord droit ('3')
            else:
                # il faut déduire de la valeur nouvellement prise, celle de la
                # position x pour le bord droit et celle de la position y pour
                # le bord bas
                self.display.data['relative'][value[edge][0]] -= self.display.data['relative'][value[edge][1]]
        # redimensionnement de la sous-fenêtre
        self.resize(window)
        # test min et ratio à intégrer

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
            print(self.stock['0'].rect)
            self.stock['0'].rect.update(self.parent.rect.x,
                                        self.parent.rect.y,
                                        self.parent.rect.w,
                                        SubWindow.border_width)
            print(self.stock['0'].rect)
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


        class Edge(pygame.sprite.Sprite):
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

        def __init__(self, name, window, parent, func=None):
            super().__init__(name, window)
            # définition des bords de l'affichage de la sous-fenêtre
            self.borders = SubWindow.Border(self)
            SubWindow.group[self.name].add(self, self.borders)  # ##
            self.parent = parent
            # self.func = Cell(random.randint(5, 15), self.image)

        def test_side(self, cursor):
            """fonction permettant de vérifier la position du curseur sur la
            sous-fenêtre, elle change le curseur en fonction de cette position,
            optant pour un curseur de redimensionnement correspondant au bord
            sur lequel se situe le curseur.
            `cursor` est une instance de la classe Cursor."""
            def set_changes(collided):
                """fonction cherchant le curseur adéquat selon les bords de la
                sous-fenêtre en collision avec le curseur. `collided` est une
                liste contenant les sprites en collision."""
                # mis à jour du/des bord(s) à tester
                Cursor.test = collided
                # il s'agit de récupérer le nom des sprites concernés
                # par une collision avec le curseur
                collided = list((map(lambda x : x.number, collided)))
                Cursor.wall = collided
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
                # deux sprites sont collided, reste à déterminer lesquels
                else:
                    # attribution d'une valeur à l'intersection de sprites,
                    # selon leur nom pour evaluer l'angle de la sous-fenêtre
                    # qui est sous le curseur
                    value = int(''.join(collided))
                    # value vaut 3 ou 12, il s'agit donc des angles haut-droit
                    # ou bas-gauche
                    if value % 3 == 0:
                        Cursor.set_current('NESW')
                    # il ne peut alors s'agir que des angles restants,
                    # à savoir : haut-gauche ou bas-droit
                    else:
                        Cursor.set_current('NWSE')

            def check_edge(collided):
                """vérifie si la souris est toujours sur le sprite de bord
                stocké en mémoire, si non, on appelle la fonction de recherche
                pour mettre à jour la variable et l'apparence du curseur.
                `collided` est une liste contenant les sprites en collision."""
                # tester le nombre de sprites entré en collision est suffisant
                nb_collided = len(pygame.sprite.groupcollide(collided,
                                                             Cursor.test,
                                                             False, False))
                if nb_collided != len(Cursor.test):
                    set_changes(collided)

            def check_no_collision(collided):
                """vérifie si une collision avec un sprite de bord a lieu.
                `collided` est une liste contenant les sprites en collision."""
                # dans le cas où la souris est bien en collision avec au moins
                # un élément
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
    - `` () ;"""
    count = 0
    font_size = None
    dict_all = {}

    def __init__(self, name, menu_names, window):
        """méthode constructrice de la classe prenant en argument :
        `name` est une chaîne de caractères pour attribuer un nom au menu
        déroulant, `menu_names` une liste de chaînes de caractères et
        `window` l'objet pygame.Surface de la fenêtre de jeu pygame."""
        pygame.sprite.OrderedUpdates.__init__(self)

        self._layer = 10 # ## dernier

        self.content = menu_names
        self.displayed = False
        ScrollingMenu.dict_all[name] = self

        self.name = name

        self.menu = self.Menu(self)
        self.menu_option = self.MenuOption(self)

        for element in menu_names:
            SubWindow(element, window)
        Layer.all_sprites.add(self)

    @staticmethod
    def resize(window):
        liste_des_mots = [f'sub_window_{i}' for i in range(1, 5)] # inutile si on connaît le mot le plus long
        ScrollingMenu.font_size = Text.get_font_size(liste_des_mots, (round(0.1 * window.get_width()), round(0.05 * window.get_height())), 2/3)
        for instance in ScrollingMenu.dict_all.values():
            instance.menu.resize(window)
            instance.menu_option.update_rect_info()
            instance.menu_option.resize()
        # ## rechoisir taille texte ?


    class Menu(pygame.sprite.Sprite):

        def __init__(self, parent):
            self.parent = parent
            self.number = ScrollingMenu.count
            ScrollingMenu.count += 1
            self.name = parent.name
            self._layer = self.parent._layer
            pygame.sprite.Sprite.__init__(self, self.parent, Layer.scrolling_menu)
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.image = pygame.Surface((1, 1))

        def resize(self, window):
            main_window_w, main_window_h = window.get_width(), window.get_height()
            x_value = round(self.number * 0.1 * main_window_w)
            w_value = round(0.1 * main_window_w)
            h_value = round(0.05 * main_window_h)
            self.rect = pygame.Rect(x_value, 0, w_value, h_value)
            self.image = pygame.Surface(self.rect.size)

            color_theme = COLOR_THEME[Window.dict_all['space'].data['color']]
            self.image.fill(COLOR[color_theme['background']])
            pygame.draw.rect(self.image, COLOR[color_theme['border']], pygame.Rect(0, 0, w_value, h_value), SubWindow.border_width)
            text = Text.font[ScrollingMenu.font_size]['font'].render(self.name, 1, COLOR[color_theme['border']])
            self.image.blit(text, get_top_left_pos(text.get_rect(), self))


    class MenuOption(pygame.sprite.Group):
        def __init__(self, parent):
            self.parent = parent
            pygame.sprite.Group.__init__(self)
            self.update_rect_info()
            self._layer = self.parent._layer
            for i, name in enumerate(parent.content):
                self.Option(self, name, i)
            #self.parent.add(self)

        def update_rect_info(self):
            self.rect_info = self.parent.menu.rect

        def resize(self):
            for sprite in self:
                sprite.resize()

        class Option(pygame.sprite.Sprite):
            def __init__(self, parent, name, place):
                self._layer = parent._layer
                pygame.sprite.Sprite.__init__(self, parent)
                self.parent = parent
                self.name = name
                self.place = place

            def resize(self):
                self.rect = self.parent.rect_info.copy()
                self.rect.y = (self.place + 1) * self.parent.rect_info.height
                self.image = pygame.Surface(self.rect.size)
                color_theme = COLOR_THEME[Window.dict_all['space'].data['color']]
                self.image.fill(COLOR[color_theme['background']])
                pygame.draw.rect(self.image, COLOR[color_theme['border']], pygame.Rect((0, 0), (self.rect.size)), SubWindow.border_width)
                text = Text.font[ScrollingMenu.font_size]['font'].render(self.name, 1, COLOR[color_theme['border']])
                self.image.blit(text, get_top_left_pos(text.get_rect(), self))


    def create_text(self):
        ...

    def change_visibility(self):
        self.displayed = not self.displayed
        Layer.all_sprites.remove(self)
        if self.displayed:
            self.add(self.menu_option)
        else:
            self.remove(self.menu_option)
        Layer.all_sprites.add(self)

    def create_surface(self):
        """"""
        """self.surface = pygame.Surface()
        font_height = 0.05 * WINDOW_DATA['height']
        font = pygame.font.Font("others/Anton-Regular.ttf",
                                     get_font_size(font_height))"""


    def display(self, surface):
        surface.blit(self.surface, self.get_position())
