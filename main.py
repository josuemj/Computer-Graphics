import pygame
from pygame.locals import *
from gl_lb1 import Render
 
width = 960
height = 540 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)

pol_1 = [(165, 380) ,(185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
def poligono(points):
    for i in range(len(points)):
        rend.glLine(points[i], points[(i+1) % len(points)])

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
    poligono(pol_1)
    

    rend.glGenerateFrameBuffer("output.bmp")
    pygame.display.flip()   
    clock.tick(60) # 60 frame per second
    

pygame.quit()
