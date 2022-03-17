"""module temporaire codé par Solène."""

import termcolor

import colorsys
import json
import pygame
try:
    from constant import COLOR_THEME, WINDOWS, COLOR, WINDOW_DATA
    from useful import get_font_size, loop_starter_pack
except ModuleNotFoundError:
    from module.constant import COLOR_THEME, WINDOWS, COLOR, WINDOW_DATA
    from module.useful import get_font_size, loop_starter_pack


style_file_path = './backup/style_2.json'

def create_main_menu(window):
    """permet la création du visuel du menu principal."""


def update_window(window):
    WINDOW_DATA['width'] = window.get_width()
    WINDOW_DATA['height'] = window.get_height()
    try:
        for element in WINDOWS:
            Window.data[element].resize()
    except KeyError:
        pass


"""def coroutine():
    def inner(func):
        def starter(*args, **kwargs):
            generator = func(*args, **kwargs)
            next(generator)
            return generator
        return starter
    return inner"""


# @coroutine()
"""def current_mouse_on_object():
    previous = ''
    yield previous
    while True:
        for element in Window.data:
            border = element.is_border_click()
            if border != previous:
                yield element.name
                previous = element.name
            if bool(border):
                print(border)
                print(element)
                element.manual_resizing()


def get_mouse_motion_event(event):
    if event.type == pygame.MOUSEMOTION:
        yield event.pos"""


def main_menu(window):
    """fonction gérant les actions par rapport au menu principal."""
    
    update_window(window)
    Window("space")
    current_window = Window.data['space']
    
    for name in WINDOWS[1:]:
        SubWindow(name)
    update_all(window)

    print(SubWindow.above)

    proceed = True
    while proceed:
        # évènements pygame
        for event in pygame.event.get():
            window = loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                update_window(window)
                window.fill(0x000000)
                update_all(window)
            if event.type == pygame.MOUSEMOTION:
                change, current_window = Window.current_mouse_on_window(event.pos, current_window)
                if change:
                    update_all(window)
                    for element in current_window.border.values():
                        pygame.draw.rect(window, (0, 150, 0),element)
                    pygame.display.flip()


def change_color_luminosity(color, rate_of_change):
    """change la luminosité de la couleur, renvoie un tuple rgb de la couleur
    assombrie selon `rate_of_change`, un entier. `couleur` doit être un tuple
    représentant les valeurs rgb (chaque entier est compris entre 0 et 255).
    Renvoie une couleur éclaircie à la condition que `rate_of_change` soit
    négatif.
    >>> change_color_luminosity((150, 150, 150), 15)
    (135, 135, 135)
    >>> change_color_luminosity((150, 3, 204), 27)
    (130, 3, 177)"""
    red, green, blue = color
    # conversion de la couleur au format hsv plus adapté pour assombrir
    hue, saturation, lightness = colorsys.rgb_to_hsv(red, green, blue)
    # le paramètre de la luminosité est diminué de `rate_of_change`
    lightness -= rate_of_change
    # la couleur est reconvertie vers le format rgb
    temp_color = colorsys.hsv_to_rgb(hue, saturation, lightness)
    final_color = [0, 0, 0]
    for i, primary in enumerate(temp_color):
        # permet d'obtenir des valeurs entières et non les float
        # renvoyé par l'usage de la méthode hsv_to_rgb du module colorsys
        final_color[i] = round(primary)
    return tuple(final_color)


def file_directory_issue():
    """décorateur permettant de solutionner les erreurs liés aux
    chemins d'accès."""
    def inner(func):
        def wrapper(**kwargs):
            # teste si la fonction ne renvoie pas une erreur
            try:
                return func(**kwargs)
            # dan le cas où l'erreur `FileNotFound` est renvoyée
            except FileNotFoundError:
                # le premier argument de la fonction est changée
                # afin que le chemin d'accès désigne le répertoire
                # parent
                kwargs['file_path'] = './.' + kwargs['file_path']
                return func(**kwargs)
        return wrapper
    return inner


def update_all(window):
    for name in WINDOWS:
        Window.data[name].display(window)
    pygame.display.flip()
    print('window updated')


def update_window_color():
    """"""


@file_directory_issue()
def get_dict(file_path):
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)
    file.close()
    return data

@file_directory_issue()
def write(file_path, dict_key, new_data):
    """"""
    data = get_dict(file_path=file_path)
    data[dict_key] = new_data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_value(file_path, key):
    """"""
    data = get_dict(file_path=file_path)
    return data[key]


class ScrollingMenu:
    """modélise un bouton permettant d'afficher au survol de la souris des
    options d'affichage ou autres. Chaque option est graphiquement défini
    comme une ligne contenant dans l'ordre : image (optionnelle), label, signe
    (correspondant à un signe de validation, pas toujours apparent, dépend des
    choix du joueur).
    
    ATTRIBUTS:
    - `` () ;
    - `` () ;
    - `` () ;
    - `` () ;
    - `` () ;
    """

    def __init__(self, menu_content):
        """méthode constructrice."""
        self.content = menu_content
    
    def create_surface(self):
        """"""
        self.surface = pygame.Surface()
        font_height = 0.05 * WINDOW_DATA['height']
        font = pygame.font.Font("others/Anton-Regular.ttf",
                                     get_font_size(font_height))

    
    def display(self, surface):
        surface.blit(self.surface, self.get_position())


class Window:
    """"""
    data =  {}

    def __init__(self, name):
        """méthode constructrice."""
        self.name = name
        self.data = get_value(file_path=style_file_path, key=name)
        Window.data[name] = self
        self.resize()
    
    def resize(self):
        """"""
        main_window_w, main_window_h = WINDOW_DATA['width'], WINDOW_DATA['height']
        x_value = round(self.data['relative']['x'] * main_window_w)
        y_value = round(self.data['relative']['y'] * main_window_h)
        w_value = round(self.data['relative']['w'] * main_window_w)
        h_value = round(self.data['relative']['h'] * main_window_h)
        self.rect = pygame.Rect(x_value, y_value, w_value, h_value)
        # Window.data[self.name]['margin'] = self.data['margin'] * main_window_h
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.Surface((self.get_width()+1, self.get_height()+1))
        color_theme = COLOR_THEME[self.data['color']]
        self.surface.fill(COLOR[color_theme['background']])
        self.border = {'up': pygame.Rect(self.get_x(),
                                         self.get_y(),
                                         self.get_width(),
                                         3),
                       'right': pygame.Rect(self.get_x()+self.get_width(),
                                            self.get_y(),
                                            3,
                                            self.get_height()),
                       'bottom': pygame.Rect(self.get_x(),
                                             self.get_height()+self.get_y(),
                                             self.get_width(),
                                             3),
                       'left': pygame.Rect(self.get_x(),
                                           self.get_y(),
                                           3,
                                           self.get_height()),
                       'upper_left': pygame.Rect(self.get_x()-3,
                                                 self.get_y()-3,
                                                 7,
                                                 7),
                       'upper_right': pygame.Rect(self.get_x()+self.get_width()-3,
                                                  self.get_y()-3,
                                                  7,
                                                  7),
                       'bottom_left': pygame.Rect(self.get_x()-3,
                                                  self.get_height()+self.get_y()-3,
                                                  7,
                                                  7),
                       'bottom_right': pygame.Rect(self.get_x()+self.get_width()-3,
                                                   self.get_height()+self.get_y()-3,
                                                   7,
                                                   7)}
    
    def display(self, surface):
        surface.blit(self.surface, self.get_position())
    
    @staticmethod
    def current_mouse_on_window(mouse_position, previous):
        for name in WINDOWS[1:]:
            if Window.data[name].is_mouse_over(mouse_position):
                if Window.data[name] != previous:
                    # renvoie la valeur de la fenêtre actuelle
                    return True, Window.data[name]
        # la souris est toujours sur la fenêtre actuelle
        return False, previous
    
    def is_mouse_over(self, mouse_position):
        """renvoie un booléen, True si un clic est effectué sur la
        sous-fenêtre, autrement la fonction renvoie False."""
        return self.rect.collidepoint(mouse_position)

    def get_position(self):
        """revoie un tuple de positions"""
        return (self.rect.x, self.rect.y)

    def get_size(self):
        """renvoie un tuple correspondant aux dimensions de la fenêtre,
        longueur puis largeur en nommbre de pixel."""
        return (self.rect.w, self.rect.h)
    
    def get_width(self):
        """renvoie le nombre de pixel en largeur."""
        return self.rect.w
    
    def get_height(self):
        """renvoie la hauteur de la fenêtre en nombre de pixel."""
        return self.rect.h
    
    def get_x(self):
        return self.rect.x
    
    def get_y(self):
        return self.rect.y


class SubWindow(Window):
    """modélise une sous-fenêtre déplaçable et redimensionnable s'apparentant
    à une surface.
    
    ATTRIBUTS:
    - `` () ;
    - `name` (str) ;
    - `relative_pos_values` (dict) ;
    - `surface` (pygame.Surface) ;
    """
    above = {}

    def __init__(self, name):
        super().__init__(name)
        self.displayed = True
        self.test_above()
    
    def manual_resizing(self):
        """"""
    
    def test_above(self):
        is_over = []
        for element in Window.data.values():
            if self.rect.colliderect(element.rect):
                is_over.append(element.name)
        SubWindow.above[self.name] = is_over
    
    def is_border_click(self, mouse_position): # ## ajouter le côté
        x_coordinate, y_coordinate = mouse_position
        for border, element in self.border.items():
            if element.collidepoint(x_coordinate, y_coordinate):
                return border
        return ''

    def create_surface(self):
        super().create_surface()
        color_theme = COLOR_THEME[self.data['color']]
        pygame.draw.circle(self.surface, color_theme['border'], (self.get_width() - 15, 15), 10, 1)
        # dessin  de l'encadré
        pygame.draw.rect(self.surface, color_theme['border'], pygame.Rect(0, 0, self.get_width(), self.get_height()), 2)
        #définition des bords dans un dictionnaire

    def update_value(self):
        """"""
    
    def change_visibility(self):
        """"""
        self.displayed = False


"""class Border: ??

    def __init__(self, object):
        self.up = pygame.Rect(self.get_x(), self.get_y(), self.get_width(), 3)
        self.right = pygame.Rect(self.get_x()+self.get_width(), self.get_y(), 3, self.get_height())
        self.bottom = pygame.Rect(self.get_x(), self.get_height()+self.get_y(), self.get_width(), 3)
        self.left = pygame.Rect(self.get_x(), self.get_y(), 3, self.get_height())
        self.corner = """