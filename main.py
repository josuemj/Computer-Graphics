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
pol_3 = [(377, 249), (411, 197), (436, 249)]
pol_4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)
]

pol_5 = [(682, 175), (708, 120), (735, 148), (739, 170)
]

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
    
    #star
    rend.glColor(0,1,1)
    poligono(pol_1)
    rend.glFillPolygon(pol_1)  
    
    #quad
    rend.glColor(0.125,1,0)
    poligono(pol_2)
    rend.glFillPolygon(pol_2) 

    #Triangle
    rend.glColor(0.9,0.3,0.3)
    poligono(pol_3)
    rend.glFillPolygon(pol_3)

    #lamp
    rend.glColor(1,1,0)
    poligono(pol_4)
    rend.glFillPolygon(pol_4)

    #whole inside lamp
    rend.glColor(0, 0, 0)
    poligono(pol_5)
    rend.glFillPolygon(pol_5)
    
    

    rend.glGenerateFrameBuffer("output.bmp")
    pygame.display.flip()   
    clock.tick(60) # 60 frame per second
    

pygame.quit()
