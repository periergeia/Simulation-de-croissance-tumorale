import math
import pygame
import pygame.freetype
try:
    from constant import COLOR_THEME
    from handle_json import get_value
    from mode import style
except:
    from module.constant import COLOR_THEME
    from module.handle_json import get_value
    from module.mode import style


pygame.init()



class SubWindow(pygame.sprite.Sprite):

    button_radius = 0

    def __init__(self, name, window):
        pygame.sprite.Sprite.__init__(self)
        # récupération des données de la sous-fenêtre
        self.data = get_value(file_path=f'./other/style_{style}.json', key=name)
        
        # self.image = pygame.Surface((100, 100))
        # self.image.fill((255, 0, 0))
        # self.rect = self.image.get_rect(center=(200, 200))
        self.button_size_change(window)
        self.resize(window)
        self.displayed = True
    
    @staticmethod
    def button_size_change(window):
        SubWindow.button_radius = math.sqrt(window.get_width() // 50 + window.get_height() // 50)
    
    def resize(self, window):
        """"""
        main_window_w, main_window_h = window.get_width(), window.get_height()
        x_value = round(self.data['relative']['x'] * main_window_w)
        y_value = round(self.data['relative']['y'] * main_window_h)
        w_value = round(self.data['relative']['w'] * main_window_w)
        h_value = round(self.data['relative']['h'] * main_window_h)
        self.rect = pygame.Rect(x_value, y_value, w_value, h_value)
        self.image = pygame.Surface(self.rect.size)

        color_theme = COLOR_THEME[self.data['color']]
        # dessin du bouton de la sous-fenêtre
        button_pos = (self.rect.width - SubWindow.button_radius * 1.5,
                      SubWindow.button_radius * 1.5)
        pygame.draw.circle(self.image, color_theme['border'], button_pos,
                           SubWindow.button_radius, 1)
        # dessin  de l'encadré
        pygame.draw.rect(self.image, color_theme['border'], pygame.Rect((0, 0), self.rect.size), 2)
        #définition des bords dans un dictionnaire
        self.border = Border(self.rect)
    
    def update(self):
        """"""


class Border(pygame.sprite.Sprite):
    def __init__(self, surface_rect):
        """self.up = pygame.Rect(self.get_x(), self.get_y(), self.get_width(), 3)
        self.right = pygame.Rect(self.get_x()+self.get_width(), self.get_y(), 3, self.get_height())
        self.bottom = pygame.Rect(self.get_x(), self.get_height()+self.get_y(), self.get_width(), 3)
        self.left = pygame.Rect(self.get_x(), self.get_y(), 3, self.get_height())
        # ##self.corner = """
        # surface_rect.outline()
    
    @property
    def up(self):
        return ...
    
    def update(self):
        pygame.sprite.spritecollide(entité, groupe, False)


class Cursor:
    def __init__(self):
        s1 = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENS)
        s2 = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
        s3 = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENESW)
        s4 = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEWE)
        self.cursors = [s1, s2, s3, s4]
        self.current = 0
    
    def update(self):
        # if pygame.mouse.get_pos():
        pygame.mouse.set_cursor(self.cursors[int(self.current)])
        self.current += 0.1


class ScrollingMenu(pygame.sprite.Sprite):
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
        """self.surface = pygame.Surface()
        font_height = 0.05 * WINDOW_DATA['height']
        font = pygame.font.Font("others/Anton-Regular.ttf",
                                     get_font_size(font_height))"""

    
    def display(self, surface):
        surface.blit(self.surface, self.get_position())