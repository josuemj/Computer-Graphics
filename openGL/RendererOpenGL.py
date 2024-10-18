import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.SetShaders(vertex_shader, fragment_shader)
#triangle positions         #color
# triangle = [-0.5, -0.5, 0,  1, 0, 0,
#             0, 0.5, 0,      0, 1, 0,
#             0.5, -0.5, 0,   0, 0, 1        
#             ]

# rend.scene.append(Buffer(triangle))

faceModel = Model("models/model.obj")
rend.scene.append(faceModel)

isRunnig = True

while isRunnig:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunnig = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunnig = False
    deltaTime = clock.tick(60) / 1000
    print(deltaTime)
    
    rend.Render()
    pygame.display.flip()
    
pygame.quit()

#skeleton