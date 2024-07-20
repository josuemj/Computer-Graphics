import pygame
from pygame.locals import *
from gl import Render

width = 960
height = 540 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock()
rend = Render(screen)
rend.glColor(1,0,1)
rend.glClear(1,0.3,1)

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN: #for keep the keyword down
            if event.type == pygame.K_ESCAPE:
                isRunning = False
    
    rend.glPoint(480, 300) # linea
    rend.glColor(1,0,0.5)
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()