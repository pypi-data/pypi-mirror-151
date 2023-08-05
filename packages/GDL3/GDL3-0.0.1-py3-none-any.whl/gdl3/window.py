import pygame


def create_win(width=500,height=500):
    game_title()
    icon()
    return pygame.display.set_mode((width,height))

def close_window():
    return pygame.QUIT

def check_event(event):
    for e in pygame.event.get():
        if e.type == event:
            return True
        
    return False

def game_title(title="GC3 Gameing"):
    pygame.display.set_caption(title)

def icon(img='gc3/logo.png'):
    imgg = pygame.image.load(img)
    pygame.display.set_icon(imgg)