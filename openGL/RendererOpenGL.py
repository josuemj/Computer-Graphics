import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

width = 1000
height = 1000

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
faceModel.AddTexture("textures/model.bmp")
rend.scene.append(faceModel)
faceModel.rotation.y = 180
isRunnig = True

while isRunnig:
    deltaTime = clock.tick(60) / 1000
    
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunnig = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunnig = False
    # print(deltaTime)

    if keys[K_LEFT]:
        faceModel.rotation.y -= 40 * deltaTime
        
    if keys[K_RIGHT]:
        faceModel.rotation.y += 40 * deltaTime
    
    rend.Render()
    pygame.display.flip()
    
pygame.quit()

#skeleton