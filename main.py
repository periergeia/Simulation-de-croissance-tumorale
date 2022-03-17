"""fichier comportant la boucle principale."""


import pygame
import pygame.freetype
from module.solene import main_menu


# initialisation de pygame
pygame.init()


# définition de variables de fenêtre
FULLSCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][1]
WINDOW_HEIGHT = round(FULLSCREEN_WIDTH * 2/3)
WINDOW_WIDTH = round(WINDOW_HEIGHT * 1.8)
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


# définition de la fenêtre pygame de taille dynamique
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)


# importation d'image
icon = pygame.image.load("./image/logo.ico").convert_alpha()


# personnalisation de la fenêtre
pygame.display.set_caption("Simulation de la croissance de cellules tumorales")
pygame.display.set_icon(icon)


if __name__ == "__main__":
    main_menu(window)
