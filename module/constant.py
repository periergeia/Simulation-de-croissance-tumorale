"""module contenant les constantes."""


OBJETS = {}
in_functions_dic = lambda f: OBJETS.setdefault(f.__name__, f)


COLOR = {'RED': (237, 41, 57),
         'ORANGE': (255, 121, 0),
         'YELLOW': (254, 203, 0),
         'GREEN': (105, 190, 40),
         'CYAN': (0, 159, 218),
         'BLUE': (0, 101, 189),
         'PURPLE': (149, 45, 152),
         'WHITE': (255, 255, 255),
         'BLACK': (0, 0, 0),
         'GOLD': (245, 189, 2),
         'SILVER': (187, 194, 204),
         'BRONZE':(205, 127, 50),
         'DARK': (0, 0, 0),
         'LIGHT_GREY': (100, 100, 100),
         'GREY': (50, 50, 50)}


COLOR_THEME = {'default': {'background': 'LIGHT_GREY',
                           'font': 'ORANGE',
                           'border': 'WHITE'},
               'dark': {'background': 'GREY',
                        'font': 'WHITE',
                        'border': 'WHITE'}}

SUBWINDOWS_NAMES = ['coeur', 'poumon', 'foie', 'colon', 'intestins', 'estomac']
