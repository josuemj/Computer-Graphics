import pygame
from pygame.locals import *
from gl import *
from obj import Obj
from model import Model
from shaders import vertexShader
import random

 
width = 512
height = 512 

screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock() 
rend = Render(screen)
rend.vertexShader = vertexShader

modelo1 = Model('face.obj')
modelo1.translate[2]= -5
modelo1.translate[1] = -1
modelo1.scale[0] = 0.1
modelo1.scale[1] = 0.1
modelo1.scale[2] = 0.1

rend.models.append(modelo1)


# triangle1 = [ [10, 80], [50, 160], [70, 80]]
# triangle2 = [ [180, 50], [150, 1], [70, 180]]
# triangle3 = [ [180, 120], [120,160], [150, 160]]


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN: #for keep the keyword down

            if event.type == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 1
                #modelo1.rotate[1] += 10
            elif event.key == pygame.K_LEFT:
                #modelo1.rotate[1] -= 10
                rend.camera.translate[0] -= 1

            
            elif event.key == pygame.K_UP:
                #modelo1.rotate[0] += 10
                rend.camera.translate[1] += 1
            elif event.key == pygame.K_DOWN:
                #modelo1.rotate[0] -= 10
                rend.camera.translate[1] -= 1

            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS

            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES

                # modelo1.scale[0] += 1
                # modelo1.scale[1] += 1
                # modelo1.scale[2] += 1
                pass
            
            elif event.key == pygame.K_0:
                # modelo1.scale[0] -= 1
                # modelo1.scale[1] -= 1
                # modelo1.scale[2] -= 1
                pass
                        
    #rend stuff
    rend.glClear()
    # rend.glTriangle(triangle1[0], triangle1[1], triangle1[2])
    # rend.glTriangle(triangle2[0], triangle2[1], triangle2[2])
    # rend.glTriangle(triangle3[0], triangle3[1], triangle3[2])
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