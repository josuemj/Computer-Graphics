import pygame
from pygame.locals import *
from gl import Render
 
width = 960
height = 540 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)


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
    
    #To big slope
    #rend.glLine((100,100), (150, 450))  
    
    punto0 = (width / 2, height / 2)

    for x in range(0, width, 20):
        rend.glColor(0.199,0.117,0.117) #color attempt
        rend.glLine((0,0), (x,height))

        rend.glLine((0,height - 1), (x,0))
        rend.glLine((width-1, 0), (x,height))
        rend.glLine((width - 1,height - 1), (x,0))


    pygame.display.flip()   
    clock.tick(60) # 60 frame per second

pygame.quit()
