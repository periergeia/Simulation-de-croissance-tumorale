"""module contenant des fonctions diverses utiles (un peu le but de
chaque fonction)."""


import pygame
import pygame.freetype


pygame.init()


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


def get_top_left_pos(rect, sprite):
    """`sprite` est une instance héritant de la classe pygame.sprite.Sprite,
    avec la condition : contenir un attribut rect. La fonction renvoie la
    position haut-gauche de l'objet rectangle `rect` sur `sprite` de sorte
    que leur centre correspondent. Il s'agit donc de centrer `rect` sur
    `sprite` et fournir la position qui nous intéresse puisque la méthode
    blit n'admet pas d'argument de destination 'center' qui aurait été
    bien pratique."""
    return (sprite.rect.width / 2 - rect.width / 2,
            sprite.rect.height / 2 - rect.height / 2)


class Text(pygame.sprite.Sprite):

    font = {}
    for number, size in {i : i * 3 + 6 for i in range(5)}.items():
        font[number] = {}
        # font[number]['font'] = pygame.font.Font("other/Montserrat.ttf", size)
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

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image = pygame.Surface((1, 1))

    @staticmethod
    def get_font_size(text, box_size, height_ratio):
        area_width, area_height = box_size
        font_height = area_height * height_ratio
        # détermination de la hauteur max du texte
        if font_height < Text.font[0]['height']:
            font_size = 0
        else:
            font_size = 0
            try:
                while font_height >= Text.font[font_size]['height']:
                    font_size += 1
            except IndexError:
                pass
        # réduction de la taille de font selon la largeur du texte
        if font_size != 0:
            try:
                while Text.font[font_size]['font'].size(text)[0] > area_width:
                    font_size -= 1
            except:
                pass
        return font_size

    @staticmethod
    def find_text_size(rect, text_list):
        # recherche du texte le plus long
        temp = {len(e): i for i, e in enumerate(text_list)}
        longest_text = text_list[temp[max(temp.keys())]]
        # obtention de la taille de font de ce texte
        Text.get_font_size(longest_text, rect.size, 2/3)

    def resize(self, font_size=None):  # ## :/
        """récupère une valeur de taille de police selon `font_height` un entier
        naturel représentant la hauteur de font voulu en nombre de pixel sur la
        fenêtre de jeu."""  # ##
        if font_size is None:
            font_size = Text.get_font_size(self.content, self.parent.rect, self.height_ratio)
        self.image = Text.font[font_size]['font'].render(self.content, 1, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.parent.rect.center)
        print("taille de font :  ", font_size)
