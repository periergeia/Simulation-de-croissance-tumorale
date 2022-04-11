"""module contenant des classes d'objet utiles à la gameplay.""" 

import pygame


class ColorTheme:  # ## pourrait être pratique
    def __init__(self):
        ...


class Cursor(pygame.sprite.Sprite):
    
    """modélise le curseur de la fenêtre de jeu.
    
    ATTRIBUTS DE CLASSE:
    - `cursors` (dict) ;
    - `test` (None | list) ;
    - `resizing` (bool) ;
    - `current` (str) ;
    - `` () ;

    ATTRIBUTS:
    - `` () ;
    - `` () ;
    - `` () ;
    - `` () ;
    - `` () ;
    """

    cursors = {'default': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW),
               'NS': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENS),
               'WE': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEWE),
               'NWSE': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENWSE),
               'NESW': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENESW)} 
    test = None
    current = cursors['default']
    resizing = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill((0, 150, 0))
        self.mask = pygame.mask.from_surface(self.image) # ##
        self.rect = pygame.Rect(0, 0, 1, 1)

    @staticmethod
    def set_current(name):
        """méthode mutatrice redéfinissant les attributs de classe current et
        resizing."""
        Cursor.current = name
        pygame.mouse.set_cursor(Cursor.cursors[name])
        # si le curseur est celui par défaut, il ne s'agit pas d'un curseur
        # pour le redimensionnement donc Cursor.resizing sera défini comme
        # False, autrement, l'attrbut de classe vaut True
        Cursor.resizing = Cursor.current != 'default'

    def update(self):
        """met à jour les coordonnées du rect pygame associé au sprite."""
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, screen):  # ##
        screen.blit(self.image,(self.rect.x, self.rect.y))


class Layer:

    stock = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates()
    windows = pygame.sprite.Group()

    @staticmethod
    def find(sprite):
        """renvoie l'indexe de calque de `sprite` un objet pygame.sprite.Sprite
        dans le groupe de sprites Layer.all_sprites."""
        try:
            # stocke le calque de plus haut indexe
            index = Layer.all_sprites.layers()[-1]
            while index >= 0:
                layer_group = pygame.sprite.Group(Layer.all_sprites.get_sprites_from_layer(index))
                if pygame.sprite.spritecollideany(sprite, layer_group, collided=None) is not None:
                    return index + 1
                index -= 1
        # erreur raised lorsque Layer.all_sprites est vide
        except IndexError:
            return 0

    @staticmethod
    def test():
        print('----')
        for index in Layer.all_sprites.layers():
            print(index)
            for sprite in Layer.all_sprites.get_sprites_from_layer(index):
                print(sprite.name)
            print('----')
    
    @staticmethod
    def test():
        for index in Layer.all_sprites.layers():
            print(index)
            for sprite in Layer.all_sprites.get_sprites_from_layer(index):
                print(type(sprite))
            print('----')

    @staticmethod
    def mouse_over():
        try:
            sprites_below = Layer.all_sprites.get_sprites_at(pygame.mouse.get_pos())
            return sprites_below[-1].name
        except IndexError:
            return None
