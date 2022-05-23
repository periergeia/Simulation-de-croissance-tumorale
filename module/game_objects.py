"""module contenant des classes d'objets utiles à la gameplay.""" 


import pygame


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
    - `` () ."""

    cursors = {'default': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW),
               'NS': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENS),
               'WE': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEWE),
               'NWSE': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENWSE),
               'NESW': pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENESW)}
    wall = None
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
    def get_resizing_status():
        return Cursor.resizing

    @staticmethod
    def set_current(name):
        """méthode mutatrice redéfinissant les attributs de classe current et
        resizing."""
        Cursor.current = name
        pygame.mouse.set_cursor(Cursor.cursors[name])
        # si le curseur est celui par défaut, il ne s'agit pas d'un curseur
        # pour le redimensionnement donc Cursor.resizing sera défini comme
        # False, autrement, l'attribut de classe vaut True
        new_value = Cursor.current != 'default'
        # dans le cas où cette nouvelle valeur est différente de l'actuelle
        if Cursor.resizing != new_value:
            # soulève un nouvel évènement dans la queue des events pygame 
            pygame.event.post(pygame.event.Event(pygame.USEREVENT+2, state=new_value, side=name))
        Cursor.resizing = new_value

    def update(self):
        """met à jour les coordonnées du rect pygame associé au sprite."""
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, screen):  # ##
        screen.blit(self.image,(self.rect.x, self.rect.y))


class Layer:

    stock = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates()
    windows = pygame.sprite.Group()  # ##
    scrolling_menus = pygame.sprite.Group()
    menu_options = pygame.sprite.Group()

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
        for index in Layer.all_sprites.layers():
            print(index)
            for sprite in Layer.all_sprites.get_sprites_from_layer(index):
                try:
                    print(sprite.name, ' '*5, type(sprite))
                except AttributeError:
                    print(' '*15, type(sprite))
            print('----')

    @staticmethod
    def move_to_top(sprite):
        """for spr in sprite:
            Layer.all_sprites.move_to_front(spr)"""
        Layer.all_sprites.remove(Layer.scrolling_menus)
        if sprite.get_layer_of_sprite() == Layer.all_sprites.get_top_layer():
            Layer.all_sprites.remove(sprite)
            Layer.all_sprites.add(sprite)
        Layer.all_sprites.add(Layer.scrolling_menus)

    @staticmethod
    def mouse_over():
        try:
            sprites_below = Layer.all_sprites.get_sprites_at(pygame.mouse.get_pos())
            return sprites_below[-1].name
        except IndexError:
            return None



"""
 change_layer(self, sprite, new_layer)
 |      change the layer of the sprite
 |
 |      LayeredUpdates.change_layer(sprite, new_layer): return None
 |
 |      The sprite must have been added to the renderer already. This is not
 |      checked.
 
 |  get_layer_of_sprite(self, sprite)
 |      return the layer that sprite is currently in
 |
 |      If the sprite is not found, then it will return the default layer.
 
 |  get_sprites_from_layer(self, layer)
 |      return all sprites from a layer ordered as they where added
 |
 |      LayeredUpdates.get_sprites_from_layer(layer): return sprites
 |
 |      Returns all sprites from a layer. The sprites are ordered in the
 |      sequence that they where added. (The sprites are not removed from the
 |      layer.
 
 |  get_top_layer(self)
 |      return the top layer
 |
 |      LayeredUpdates.get_top_layer(): return layer
 
 |  get_top_sprite(self)
 |      return the topmost sprite
 
 |  move_to_front(self, sprite)
 |      bring the sprite to front layer
 |
 |      LayeredUpdates.move_to_front(sprite): return None
 |
 |      Brings the sprite to front by changing the sprite layer to the top-most
 |      layer. The sprite is added at the end of the list of sprites in that
 |      top-most layer.
 
 |  switch_layer(self, layer1_nr, layer2_nr)
 |      switch the sprites from layer1_nr to layer2_nr
 |
 |      LayeredUpdates.switch_layer(layer1_nr, layer2_nr): return None
 |
 |      The layers number must exist. This method does not check for the
 |      existence of the given layers."""
