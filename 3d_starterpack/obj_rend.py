import pygame
from pygame.locals import *
from gl import Render
from obj import Obj
from model import Model
from shaders import vertexShader
 
width = 960
height = 540 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)
rend.vertexShader = vertexShader

modelo1 = Model('face.obj')
modelo1.translate[0] = width / 2
modelo1.translate[1] = height / 4

modelo1.scale[0] = 10
modelo1.scale[1] = 10
modelo1.scale[2] = 10


rend.models.append(modelo1)

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN: #for keep the keyword down
            if event.type == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 10
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 10
    #rend stuff

    rend.glClear()
    rend.glRender()
    
    #To big slope
    #rend.glLine((100,100), (150, 450))  
    
    #punto0 = (width / 2, height / 2)

    # for x in range(0, width, 20):
    #     rend.glColor(1,0.5,1) #color attempt
    #     rend.glLine((0,0), (x,height))

    #     rend.glLine((0,height - 1), (x,0))
    #     rend.glLine((width-1, 0), (x,height))
    #     rend.glLine((width - 1,height - 1), (x,0))

    rend.glGenerateFrameBuffer("output.bmp")
    pygame.display.flip()   
    clock.tick(60) # 60 frame per second
    

pygame.quit()
