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

faceModel = Model("models/LionSculpture.obj")
faceModel.AddTexture("textures/ModelTexture.bmp")
faceModel.translation.z = -5
faceModel.translation.y = -1

faceModel.scale.x = 3
faceModel.scale.y = 3
faceModel.scale.z = 3
rend.scene.append(faceModel)


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
            
            elif event.key == pygame.K_1:
                rend.SetShaders(grayscale_vertex_shader, grayscale_shader)
            
            elif event.key == pygame.K_2:
                rend.SetShaders(edge_detection_vertex_shader, grayscale_shader)
            
            elif event.key == pygame.K_3:
                rend.SetShaders(toon_vertex_shader, rainbow_shader)
            
            elif event.key == pygame.K_4:
                rend.SetShaders(rainbow_vertex_shader, rainbow_shader)
            
            elif event.key == pygame.K_5:
                rend.SetShaders(bounce_vertex_shader, orange_fragment_shader)
            
            elif event.key == pygame.K_6:
                rend.SetShaders(pulse_vertex_shader, orange_fragment_shader)
                
    # print(deltaTime)

    if keys[K_LEFT]:
        faceModel.rotation.y -= 40 * deltaTime
        
    if keys[K_RIGHT]:
        faceModel.rotation.y += 40 * deltaTime
        
    #camera
    if keys[K_a]:
        rend.camera.position.x -= 1 * deltaTime #1m/s
    
    if keys[K_d]:
        rend.camera.position.x += 1 * deltaTime #1m/s
    
    if keys[K_w]:
        rend.camera.position.y += 1 * deltaTime #1m/s
    
    if keys[K_s]:
        rend.camera.position.y -= 1 * deltaTime #1m/s
    
    
    rend.time += deltaTime
    
    rend.Render()
    pygame.display.flip()
    
pygame.quit()

#skeleton