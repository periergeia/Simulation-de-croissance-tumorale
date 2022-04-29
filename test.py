import pygame
from random import randint, random


class Grid:

    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (255, 255, 255)
        self.win_width = self.screen.get_width()
        self.win_height = self.screen.get_height()
        self.color = (0, 0, 0)
        self.block_size = 20

    def draw_grid(self):
        self.screen.fill(self.bg_color)
        for x in range(0, self.win_width, self.block_size):
            pygame.draw.line(self.screen, self.color, (x, 0), (x, self.win_height))
            pygame.draw.line(self.screen, self.color, (0, x), (self.win_width, x))


class Cell(pygame.sprite.Sprite):
    """
    Définit l'objet Cellule
    """
    image = pygame.image.load(f'assets/sprite/cell_sprite.png')
    group = pygame.sprite.Group()

    def __init__(self, pos, size):
        """
        Initialise la position de la cellule
        """
        pygame.sprite.Sprite.__init__(self, Cell.group)
        self.color = (0, 0, 0)
        self.image = Cell.image
        self.size = size
        self.rect = pygame.Rect(pos, self.size)
        self.pos = pos
        self.neighbors = []

    def test_neighbors(self, new_pos):
        for cell in Cell.group:
            if new_pos == cell.get_pos() or new_pos == self.pos:
                return True
        return False

    def dup_cell(self):
        """
        Renvoie la position d'une cellule dupliquée sous forme de tuple(x, y)
        définie de manière aléatoire
        """
        rand = random()
        if rand < 10**(-2):
            new_pos = self.pos[0] + randint(-1, 1) * self.size[0], self.pos[1] + randint(-1, 1) * self.size[0]
            if not Cell.test_neighbors(self, new_pos):
                return new_pos
        return

    def update(self):
        self.topleft = (self.pos_x, self.pos_y)

    def get_pos(self):
        """
        Renvoie la position de l'objet.
        """
        return self.pos


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Test")

        self.grid = Grid(self.screen)
        self.cell = Cell((self.screen.get_width()//2, self.screen.get_height()//2), (20, 20))

    def gen_cells(self):
        list_cells = Cell.group
        for cell in list_cells:
            new_cell_pos = cell.dup_cell()
            if new_cell_pos is not None:
                Cell(new_cell_pos, (20, 20))

    def draw_cells(self):
        Cell.group.draw(self.screen)

    def update(self):
        self.grid.draw_grid()

    def run(self):
        clock = pygame.time.Clock()

        jeu = True
        while jeu:

            self.gen_cells()
            self.update()
            self.draw_cells()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jeu = False

            clock.tick(60)
            pygame.display.set_caption(f'FPS : {clock.get_fps()}')
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
