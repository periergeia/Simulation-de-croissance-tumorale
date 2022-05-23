"""Module contenant les classes :
- Window ;
- SubWindow ;
- ScrollingMenu
pour la gestion des objets modélisant des fenêtres du jeu."""


# importations des différents modules
import math
import pygame
try:
    from constant import FUNCTION, COLOR_THEME, COLOR, in_functions_dict
    from game_objects import Cursor, Layer
    from handle_json import get_value
    from mode import style
    from useful import get_top_left_pos, Text
except ModuleNotFoundError:
    from module.constant import FUNCTION, COLOR_THEME, COLOR, in_functions_dict
    from module.game_objects import Cursor, Layer
    from module.handle_json import get_value
    from module.mode import style
    from module.useful import get_top_left_pos, Text


# initialisation du module pygame
pygame.init()


class Image(pygame.sprite.Sprite):

    group = {} 

    def __init__(self, file_path, parent_name, relative_position, name=None):
        self._layer = Window.dict_all[parent_name]._layer
        pygame.sprite.Sprite.__init__(self, Layer.all_sprites)
        self.image_save = pygame.image.load(file_path).convert_alpha()
        self.image = self.image_save.copy()
        self.parent_name = parent_name
        self.name = name
        self.relative_position = relative_position
        self.rect = pygame.Rect(0, 0, 0, 0)
        Image.group[name] = self
        self.resize(1)

    def resize(self, windows):
        window_size = Window.dict_all[self.parent_name].rect.size
        window_pos = Window.dict_all[self.parent_name].rect.topleft
        x_value = self.relative_position[0] * window_size[0]
        y_value = self.relative_position[1] * window_size[1]
        w_value = round(self.relative_position[2] * window_size[0])
        h_value = round(self.relative_position[3] * window_size[1])
        self.rect.update(x_value + window_pos[0], y_value + window_pos[1], w_value, h_value)
        self.image = pygame.transform.smoothscale(self.image_save, (w_value, h_value))


class Graphical(pygame.sprite.Group):
    """"""
    def __init__(self, name, parent):
        pygame.sprite.Group.__init__(self)
        #self.refresh = 1/timer
        #self.change_image(window)
        self.background = Image(f"./image/{name}.png", name, parent.data['image'])
        self.add(self.background)

    def resize(self):
        self.background.resize(1)

    def change_image(self, window):
        ...
        """size = random.randint(10, min(window.get_size())//2)
        self.image = pygame.Surface(window.get_size())
        self.image.set_colorkey((0, 0, 0))
        random_color = (random.randint(size, 255), random.randint(size, 255), random.randint(0, 255))
        random_position = (random.randint(0, window.get_width()-size), random.randint(0, window.get_height()-size))
        pygame.draw.circle(self.image, random_color, random_position,size)
        font = pygame.font.Font(None, get_font_size(size))
        self.image.blit(font.render(str(self.id), 1, (0, 150, 0)), (0, 0))
        self.rect = self.image.get_rect()"""

    """def update(self, window):
        self.state += self.refresh
        if self.state > 1:
            self.change_image(window)
            self.state = 0
        window.blit(self.image, (0, 0))
        return window"""


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
    - `_layer` (int) : position du calque ;
    - `data` (dict) : contient les données (position relative,
    taille relative, ...) de l'objet fenêtre récupérées dans un fichier JSON
    (précisé par le nom de la fenêtre) ;
    - `image` (pygame.Surface) : représentation graphique de l'instance ;
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
        self.mask = pygame.mask.from_surface(self.image)
        self.resize(window)
        self._layer = Layer.find(self)
        pygame.sprite.Sprite.__init__(self, Layer.all_sprites, Layer.stock)  # ##

    def resize(self, window):
        """redimensionne selon les valeurs de la fenêtre de jeu `window`, une
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
        |___Display"""

    border_width = 0
    group = {}

    def __init__(self, name, window, func):
        """méthode constructrice."""
        pygame.sprite.OrderedUpdates.__init__(self)
        SubWindow.group[name] = self
        self.displayed = False
        self.display = SubWindow.Display(name, window, self, func)
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
        color_theme = COLOR_THEME[Window.dict_all['coeur'].data['color']]
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
        """change la visibilité d'une sous-fenêtre dont le nom `name` est
        spécifié en paramètre. Si elle est visible, elle est rendue invisible,
        autrement, elle est rendue visible."""
        try:
            # dans le cas où la sous-fenêtre appartient au groupe d'affichage
            if Layer.all_sprites.has(SubWindow.group[name]):
                # la sous-fenêtre est retirée du groupe d'affichage
                Layer.all_sprites.remove(SubWindow.group[name])
            else:
                # on ajoute l'instance dans le groupe d'affichage
                Layer.all_sprites.add(SubWindow.group[name])
        except KeyError:  # ##inutile ?
            pass

    def resize(self, window):
        """méthode appelant les méthodes de redimensionnement propre à chaque
        instance de sprites de la classe."""
        # redimensionnement de tous les sprites de sous-fenêtre apparents sur
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
        dict_value = self.display.data['relative']
        min_size = self.display.data['min_size']
        # pour chaque bord en contact avec le curseur (deux au plus)
        for edge in Cursor.wall:
            # previous_relative_value peut être inutilisé dans certains cas
            # il est plus rentable que de vérifier si edge = 0 | edge = 2
            previous_relative_value = dict_value[value[edge][0]]
            # il s'agit de savoir si les valleurs changer sont dépendant de la
            # largeur ou de la longueur de la fenêtre de jeu, on rappelle que
            # tout est défini relativement à celle-ci en terme de
            # proportionnalité, x et w dépendent de la largeur tandis que y et
            # h sont selon la hauteur
            size_index = 1 if int(edge) < 2 else 0
            # changement d'une valeur qui prend en considération la position
            # de la souris et du bord
            dict_value[value[edge][0]] = pygame.mouse.get_pos()[size_index] / \
                                         window.get_size()[size_index]
            # s'il s'agit du bord haut ('0') ou du bord gauche ('2')
            if int(edge) % 2 == 0:
                # il s'agit de changer la hauteur (si bord haut)
                # (respectivement la largeur (si bord gauche)) afin de donner
                # l'illusion que la position du bord bas (respectivement bord
                # droit) reste inchangée
                diff = dict_value[value[edge][0]] - previous_relative_value
                dict_value[value[edge][1]] = dict_value[value[edge][1]] - diff
            # il ne peut que s'agir du bord bas ('1') ou du bord droit ('3')
            else:
                # il faut déduire de la valeur nouvellement prise, celle de la
                # position x pour le bord droit et celle de la position y pour
                # le bord bas
                dict_value[value[edge][0]] -= dict_value[value[edge][1]]

        # test afin que la sous-fenêtre soit contenue dans 'space'
        dict_value['y'] = 0.05 if dict_value['y'] < 0.05 else dict_value['y']
        for i in ['0', '2']:
            if dict_value[value[i][0]] + dict_value[value[i][1]] > 1:
                dict_value[value[i][1]] = 1 - dict_value[value[i][0]]

        # admissibilité des valeurs en terme
        # - de ratio
        # ##if dict_value['w'] / dict_value['h'] < min_size['ratio']:
        # ##    dict_value['w'] = round(min_size['ratio'] * dict_value['h'])
        # - de largeur
        if dict_value['h'] < min_size['h']:
            dict_value['h'] = min_size['h']
        # - de hauteur
        if dict_value['w'] < min_size['w']:
            dict_value['w'] = min_size['w']

        # redimensionnement de la sous-fenêtre
        self.resize(window)

    class Button(pygame.sprite.Sprite):
        """modélise un bouton de sous-fenêtre.

        ATTRIBUTS DE CLASSE:
        - `image` (pygame.Surface) : représentation visuelle d'un bouton ;
        - `mask` (pygame.Mask) : représentation du masque (un objet permettant
        d'estimer la surface occupée par une image) du cercle visuel servant de
        bouton de fermeture d'une sous-fenêtre;
        - `radius` (int) : il s'agit du rayon d'un bouton.

        ATTRIBUTS:
        - `_layer` (int) : calque sur lequel se situe l'instance ;
        - `name` (str) : nom du bouton pour l'associer à la sous-fenêtre ;
        - `parent` (Subwindow) : correspond à l'instance parent ;
        - `rect` (pygame.Rect) : rectangle occupé par le bouton."""

        radius = 0
        image = None
        mask = None

        def __init__(self, window_display):
            """méthode constructrice."""
            self.name = window_display.name  # ##
            self.rect = pygame.Rect(0, 0, 0, 0)  # ## moyen d'enlever
            self.parent = window_display
            self._layer = window_display._layer
            pygame.sprite.Sprite.__init__(self)

        def resize(self):
            """méthode de redimensionnement."""
            self.image = SubWindow.Button.image
            self.mask = SubWindow.Button.mask
            x_axis = self.parent.rect.x + self.parent.rect.w - 1.5 * SubWindow.Button.radius
            y_axis = self.parent.rect.y + 1.5 * SubWindow.Button.radius
            self.rect = self.image.get_rect(center=(x_axis, y_axis))

        def get_name(self):
            """renvoie le nom de la sous-fenêtre associée."""
            return self.name


    class Border(pygame.sprite.Group):
        """modélise une bordure de fenêtre, un rectangle aurait été bien plus
        simple mais l'esthétique n'y sera pas, certaines personnes aiment bien
        s'embêter (pour rush la dernière semaine avant le rendu du projet).

        ATTRIBUTS:
        - `parent` (SubWindow.Display) : surface sur laquelle nous associons
        une bordure ;
        - `stock` (dict) : contient quatre couple correspondant aux bords, des
        instances de la classe SubWindow.Border.Edge :
            - '0' : bord haut
            - '1' : bord bas
            - '2' : bord gauche
            - '3' : bord droit.

        ARCHITECTURE DE LA CLASSE:
        Border
            |___Edge"""

        def __init__(self, window_display):
            """méthode constructrice, `window_display est une instance de
            la classe `SubWindow.Display`."""
            pygame.sprite.Group.__init__(self)
            self.parent = window_display
            self.stock = {}
            layer = window_display._layer
            for edge in [str(i) for i in range(4)]:
                self.stock[edge] = self.Edge(edge, window_display.name, layer)
                self.add(self.stock[edge])

        def resize(self):
            """méthode de redimensionnement des bords de la bordure."""
            # 0 --> bord du haut (top)
            self.stock['0'].rect.update(self.parent.rect.x,
                                        self.parent.rect.y,
                                        self.parent.rect.w,
                                        SubWindow.border_width)
            # 1 --> bord du bas (bottom)
            sum_y_h = self.parent.rect.h + self.parent.rect.y
            bottom_y_axis = sum_y_h - SubWindow.border_width
            self.stock['1'].rect.update(self.parent.rect.x,
                                        bottom_y_axis,
                                        self.parent.rect.w,
                                        SubWindow.border_width)
            # 2 --> bord de gauche (left)
            self.stock['2'].rect.update(self.parent.rect.x,
                                        self.parent.rect.y,
                                        SubWindow.border_width,
                                        self.parent.rect.h)
            # 3 --> bord de droite (right)
            sum_x_w = self.parent.rect.x + self.parent.rect.w
            right_x_axis = sum_x_w - SubWindow.border_width
            self.stock['3'].rect.update(right_x_axis,
                                        self.parent.rect.y,
                                        SubWindow.border_width,
                                        self.parent.rect.h)
            self.update_image()

        def update_image(self):
            """met à jour l'attribut image de l'instance."""
            for sprite in self:
                sprite.update_image()
                sprite.image.fill(COLOR_THEME[self.parent.data['color']]['border'])


        class Edge(pygame.sprite.Sprite):
            """modélise un bord.

            ATTRIBUTS:
            - `_layer` (int) : numéro du calque ;
            - `image` (pygame.Surface) : représentation visuelle ;
            - `name` (int) : nom de la sous-fenêtre associée ;
            - `number` (int) : identifie le côté représenté par le bord :
                - '0' : bord haut
                - '1' : bord bas
                - '2' : bord gauche
                - '3' : bord droit ;
            - `rect` (pygame.Rect) : permet de situer la représentation
            visuelle par rapport à la fenêtre de jeu."""

            def __init__(self, number, name, layer):
                """méthode constructrice."""
                self.number = number
                self.name = name
                self._layer = layer
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.image = pygame.Surface((0, 0))
                pygame.sprite.Sprite.__init__(self)

            def update_image(self):
                """met à jour (à moitié) l'attribut image de l'instance."""
                self.image = pygame.Surface(self.rect.size)

            def get_name(self):
                """renvoie le nom de la sous-fenêtre associée."""
                return self.name

            def get_number(self):
                """renvoie le nombre identifiant le côté de la bordure."""
                return self.number


    class Display(Window):
        """modélise un écran de sous-fenêtre, il s'agit de la surface dépourvue
        de bouton de fermeture.

        ATTRIBUTS ISSUS DE LA CLASSE PARENT:
        - `_layer` (int) : position du calque ;
        - `data` (dict) : contient les données (position relative,
        taille relative, ...) de l'objet fenêtre récupérées dans un fichier JSON
        (précisé par le nom de la fenêtre) ;
        - `image` (pygame.Surface) : représentation graphique de l'instance ;
        - `name` (str) : nom de la fenêtre ;
        - `rect` (pygame.Rect) : défini la position et les dimensions utiles à
        l'affichage.

        ATTRIBUTS:
        - `borders` (SubWindow.Borders) : bordure de la sous-fenêtre ;
        - `parent` (SubWindow) : sauvegarde d'une référence de l'instance parent."""

        def __init__(self, name, window, parent, func):
            """méthode constructrice."""
            super().__init__(name, window)
            if func == 1:
                self.func = Graphical(name, self)
            # définition des bords de l'affichage de la sous-fenêtre
            self.borders = SubWindow.Border(self)
            SubWindow.group[self.name].add(self, self.func, self.borders)
            self.parent = parent
        
        def resize(self, window):
            super().resize(window)
            try:
                self.func.resize()
            except AttributeError:
                pass

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

            # création d'une liste des bords touchés
            collided = pygame.sprite.spritecollide(cursor, self.borders, False)
            if Cursor.test:
                check_edge(collided)
            else:
                check_no_collision(collided)

    def get_layer_of_sprite(self):
        """renvoie le numéro de calque de l'instance."""
        return self.display.layer


class ScrollingMenu(pygame.sprite.OrderedUpdates):
    """modélise un menu déroulant.

    ATTRIBUTS DE CLASSE:
    - `count` (int) : compteur, nombre d'instance créé, utile pour le placement
    sur la fenêtre de jeu ;
    - `font_size` (None | int) : taille de font à prendre ;
    - `dict_all` (dict) : contient les instances référencées par leur nom.

    ATTRIBUTS:
    - `_layer` (int) : numéro du calque (vous commencez à bien connaître) ;
    - `content` (list) : liste des menus à créer ;
    - `displayed` (bool) : visibilité de l'affichage ;
    - `menu` (ScrollingMenu.Menu) : référence vers l'objet créé ;
    - `menu_option` (ScrollingMenu.MenuOption) : référence vers l'objet créé ;
    - `name` (str) : nom du menu déroulant.

    ARCHITECTURE DE LA CLASSE:
    ScrollingMenu
        |___Menu
        |___MenuOption
            |___Option"""

    count = 0
    font_size = None
    dict_all = {}

    def __init__(self, name, menu_names, window, func=None):
        """méthode constructrice de la classe prenant en argument :
        `name` est une chaîne de caractères pour attribuer un nom au menu
        déroulant, `menu_names` une liste de chaînes de caractères et
        `window` l'objet pygame.Surface de la fenêtre de jeu pygame."""
        pygame.sprite.OrderedUpdates.__init__(self, Layer.scrolling_menus)
        self._layer = 10 # ## dernier
        self.content = menu_names
        self.displayed = False
        ScrollingMenu.dict_all[name] = self
        self.name = name
        self.menu = self.Menu(self)
        self.menu_option = self.MenuOption(self)
        # création des sous-fenêtres
        for element in menu_names:
            # dans le cas où il s'agit de fonctions spécifiques
            try:
                FUNCTION[element]()
            except KeyError:
                # création d'une sous-fenêtre
                SubWindow(element, window, func)

    @staticmethod
    def resize(window):
        """méthode de redimensionnement où `window` correspond à la surface
        de la fenêtre de jeu pygame. Elle redimensionne tous les menus
        déroulant."""
        # ## remplacer par mot le plus long de la liste des mots contenus
        # dans les menus déroulant
        longest_word = 'intestins'
        # redéfinition de la taille de la police
        rect_size = (round(0.1 * window.get_width()),
                     round(0.05 * window.get_height()))
        ScrollingMenu.font_size = Text.get_font_size(longest_word,
                                                     rect_size, 2/3)
        for instance in ScrollingMenu.dict_all.values():
            instance.menu.resize(window)
            instance.menu_option.update_rect_info()
            instance.menu_option.resize()


    class Menu(pygame.sprite.Sprite):
        """modélise le bouton de menu, celui toujours visible et permettant
        d'afficher le menu déroulant.

        ATTRIBUTS:
        - `_layer` (int) : numéro du calque ;
        - `image` (list) : représentation visuelle du bouton de menu ;
        - `name` (str) : nom du menu déroulant associé ;
        - `number` (int) : attribut pratique pour l'emplacement du bouton de
        menu selon l'ordre d'instanciation des objets de la classe
        ScrollingMenu ;
        - `parent` (ScrollingMenu) : référence vers l'instance parent ;
        - `rect` (pygame.Rect) : contient les données nécéssaires pour situer
        l'image du sprite sur la fenêtre de jeu pygame."""

        def __init__(self, parent):
            """méthode constructrice."""
            self.parent = parent
            self.number = ScrollingMenu.count
            ScrollingMenu.count += 1
            self.name = parent.name
            self._layer = self.parent._layer
            pygame.sprite.Sprite.__init__(self, self.parent,
                                          Layer.scrolling_menus)
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.image = pygame.Surface((0, 0))

        def resize(self, window):
            """méthode pour le redimensionnement."""
            main_window_w, main_window_h = window.get_size()
            x_value = round(self.number * 0.1 * main_window_w)
            w_value = round(0.1 * main_window_w)
            h_value = round(0.05 * main_window_h)
            self.rect = pygame.Rect(x_value, 0, w_value, h_value)
            self.image = pygame.Surface(self.rect.size)
            color_theme = COLOR_THEME[Window.dict_all['space'].data['color']]
            # remplissage de la surface avec la couleur de fond
            self.image.fill(COLOR[color_theme['background']])
            # ajout d'une bordure pour l'esthétique et parce que je n'ai padvi
            pygame.draw.rect(self.image, COLOR[color_theme['border']],
                             pygame.Rect(0, 0, w_value, h_value),
                             SubWindow.border_width)
            # ajout du texte
            text = Text.font[ScrollingMenu.font_size]['font']
            text_surface = text.render(self.name, 1,
                                       COLOR[color_theme['border']])
            self.image.blit(text_surface,
                            get_top_left_pos(text_surface.get_rect(), self))

        def get_name(self):
            """renvoie le nom de la sous-fenêtre associée."""
            return self.name


    class MenuOption(pygame.sprite.Group):
        """modélise un menu déroulant, bouton pour l'ouvrir et fermer exclu.

        ATTRIBUTS:
        - `_layer` (int) : numéro du calque ;
        - `parent` (ScrollingMenu) : référence vers l'instance parent ;
        - `rect_info` (pygame.Rect) : permet de transporter les informations
        du bouton associé aux options de menu afin que ce dernier puisse avoir
        des caractéristiques de position et dimensions.

        ARCHITECTURE DE LA CLASSE:
        MenuOption
            |___Option"""

        def __init__(self, parent):
            """méthode constructrice."""
            self.parent = parent
            pygame.sprite.Group.__init__(self)
            self.update_rect_info()
            self._layer = self.parent._layer
            for i, name in enumerate(parent.content):
                self.Option(self, name, i)

        def update_rect_info(self):
            """met à jour les données du rectangle de référence."""
            self.rect_info = self.parent.menu.rect

        def resize(self):
            """méthode de redimensionnement."""
            for sprite in self:
                sprite.resize()


        class Option(pygame.sprite.Sprite):
            """correspond à une option d'un menu déroulant.

            ATTRIBUTS:
            - `_layer` (int) : numéro du calque ;
            - `name` (str) : nom du menu déroulant ;
            - `parent` (ScrollingMenu) : référence vers l'instance parent ;
            - `place` (int) : position sur l'axe y, 0 correspondant au premier
            en partant du haut."""

            def __init__(self, parent, name, place):
                """méthode constructrice."""
                self._layer = parent._layer
                pygame.sprite.Sprite.__init__(self, parent, Layer.menu_options)
                self.parent = parent
                self.name = name
                self.place = place
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.image = pygame.Surface((0, 0))

            def resize(self):
                """méthode de redimensionnement."""
                self.rect = self.parent.rect_info.copy()
                self.rect.y = (self.place + 1) * self.parent.rect_info.height
                self.image = pygame.Surface(self.rect.size)
                color_theme = COLOR_THEME[Window.dict_all['space'].data['color']]
                self.image.fill(COLOR[color_theme['background']])
                pygame.draw.rect(self.image, COLOR[color_theme['border']],
                                 pygame.Rect((0, 0), (self.rect.size)),
                                 SubWindow.border_width)
                text = Text.font[ScrollingMenu.font_size]['font']
                text_surface = text.render(self.name, 1,
                                           COLOR[color_theme['border']])
                self.image.blit(text_surface,
                                get_top_left_pos(text_surface.get_rect(), self))

            def get_name(self):
                """renvoie le nom de la sous-fenêtre associée."""
                return self.name

    def change_visibility(self):
        """permet de changer la visibilité des options de menu."""
        # changement du booléen gérant l'état de la visibilité
        self.displayed = not self.displayed
        Layer.all_sprites.remove(self)
        # si les options doivent être affichées
        if self.displayed:
            # ajout des sprites des menus d'option dans l'instance
            self.add(self.menu_option)
        else:
            # les menus d'options sont retirés de l'instance
            self.remove(self.menu_option)
        # on ajoute l'instance dans le groupe d'affichage
        Layer.all_sprites.add(self)


@in_functions_dict
def el_joseph():
    """change la visibilité d'une sous-fenêtre dont le nom `name` est
    spécifié en paramètre. Si elle est visible, elle est rendue invisible,
    autrement, elle est rendue visible."""
    print('appelée')
    #try:
    # dans le cas où la sous-fenêtre appartient au groupe d'affichage
    if Layer.all_sprites.has(Image.group['sans_organe']):
        # la sous-fenêtre est retirée du groupe d'affichage
        Layer.all_sprites.remove(Image.group['sans_organe'])
        Layer.all_sprites.add(Image.group['organe'])
    else:
        # on ajoute l'instance dans le groupe d'affichage
        Layer.all_sprites.remove(Image.group['organe'])
        Layer.all_sprites.add(Image.group['sans_organe'])
    #except KeyError:  # ##inutile ?
    #    pass
