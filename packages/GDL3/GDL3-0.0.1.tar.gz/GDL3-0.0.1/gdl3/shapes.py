import pygame

def draw_circle(win,radius,x,y,color="red", borders=True):
    if borders:
        pygame.draw.circle(win, color, (x,y),radius,2)

    else:
        pygame.draw.circle(win, color, (x,y),radius)

def draw_rect(win,x,y,width,height,color="red", borders=True):
    if borders:
        pygame.draw.rect(win, color, (x,y,width,height),2)
    
    else:
        pygame.draw.rect(win, color, (x,y,width,height))
