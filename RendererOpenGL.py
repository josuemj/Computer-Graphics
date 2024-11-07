import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model

width = 960
height = 540


pygame.init()

camDistance = 5
camAngle = 0
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

skyboxTextures = [
"skybox/right.jpg",
"skybox/left.jpg",
"skybox/top.jpg",
"skybox/bottom.jpg",
"skybox/front.jpg",
"skybox/back.jpg"]

rend.CreateSkyBox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

rend.SetShaders(vertex_shader, fragment_shader)
#triangle positions         #color
# triangle = [-0.5, -0.5, 0,  1, 0, 0,
#             0, 0.5, 0,      0, 1, 0,
#             0.5, -0.5, 0,   0, 0, 1        
#             ]

# rend.scene.append(Buffer(triangle))

faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.translation.z = -5
faceModel.scale.x = 2
faceModel.scale.y = 2
faceModel.scale.z = 2
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
                rend.FilledMode()
            
            elif event.key == pygame.K_2:
                rend.WireframeMode()
            
            elif event.key == pygame.K_3:
                rend.SetShaders(vertex_shader, fragment_shader)
            
            elif event.key == pygame.K_4:
                rend.SetShaders(fat_shader, fragment_shader)
            
            elif event.key == pygame.K_5:
                rend.SetShaders(water_shader, fragment_shader)
                
    # print(deltaTime)

    if keys[K_LEFT]:
        faceModel.rotation.y -= 40 * deltaTime
        
    if keys[K_RIGHT]:
        faceModel.rotation.y += 40 * deltaTime
        
    #camera
    # if keys[K_a]:
    #     rend.camera.position.x -= 1 * deltaTime #1m/s
    
    # if keys[K_d]:
    #     rend.camera.position.x += 1 * deltaTime #1m/s
    
    # if keys[K_w]:
    #     rend.camera.position.y += 1 * deltaTime #1m/s
    
    # if keys[K_s]:
    #     rend.camera.position.y -= 1 * deltaTime #1m/s
    
    if keys[K_a]:
        camAngle -= 45 * deltaTime
        
    if keys[K_d]:
        camAngle += 45 * deltaTime
    
    if keys[K_w]:
        camDistance -= 2 * deltaTime
    
    if keys[K_s]:
        camDistance += 2 * deltaTime
        
    rend.time += deltaTime
    
    rend.camera.LookAt(faceModel.translation)
    rend.camera.Orbit(faceModel.translation, camDistance, camAngle)
    
    # rend.camera.LookAt(faceModel.translation)
    
    rend.Render()
    pygame.display.flip()
    
pygame.quit()

#skeleton