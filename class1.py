import pygame
from pygame.locals import *
from gl import Render

width = 960
height = 540 



screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)
rend.glclearColor(1,1,1)

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
    for i in range(300):
        rend.glPoint(10+i,220-i,[0.2,0.3,0.3])
   
    pygame.display.flip()
    clock.tick(60) # 60 frame per second

rend.glGenerateFrameBuffer('output.bmp')

pygame.quit()
