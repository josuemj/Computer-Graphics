import pygame
from pygame.locals import *
from gl_lb1 import Render
 
width = 960
height = 540 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)

pol_1 = [(165, 380) ,(185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
pol_2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

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

    rend.glColor(0.3,0.3,0.3)
    poligono(pol_1)
    rend.glFillPolygon(pol_1)  

    rend.glColor(0.9,0.3,0.3)
    poligono(pol_2)
    rend.glFillPolygon(pol_2) 
    
    

    rend.glGenerateFrameBuffer("output.bmp")
    pygame.display.flip()   
    clock.tick(60) # 60 frame per second
    

pygame.quit()
