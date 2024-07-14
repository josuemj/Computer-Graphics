import pygame
from pygame.locals import *
from gl import Render

width = 960
height = 540 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)
rend.glColor(1,0,1)
rend.glClearColor(1, 0.5, 1)

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN: #for keep the keyword down
            if event.type == pygame.K_ESCAPE:
                isRunning = False
    #rend stuff

    rend.glClear()
    rend.glPoint(480,270)
    for i in range(100):
        rend.glPoint(480+i,270+i)

    pygame.display.flip()   
    clock.tick(60) # 60 frame per second

pygame.quit()
