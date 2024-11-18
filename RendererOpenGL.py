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
camVerticalAngle = 0

minCamDistance = 2
maxCamDistance = 50

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

# skyboxTextures = [
# "citybox/right.png",
# "citybox/left.png",
# "citybox/up.png",
# "citybox/down.png",
# "citybox/front.png",
# "citybox/back.png"]

rend.CreateSkyBox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

rend.SetShaders(vertex_shader, fragment_shader)

snowGround = Model("models/snow.obj")
snowGround.AddTexture("textures/snow.bmp")    
snowGround.translation.z = -5
snowGround.scale.x = 10
snowGround.scale.y = 10
snowGround.scale.z = 10
# dinoModel.rotation.x -=90

rend.scene.append(snowGround)

polar = Model("models/polar.obj")
polar.AddTexture("textures/polar.bmp")
polar.translation.z = -5
# polar.translation.x = 1.4
polar.scale.x = 1.2
polar.scale.y = 1.2
polar.scale.z = 1.2
polar.translation.y = 0.95
rend.scene.append(polar)

nuclearWaste = Model("models/nuclearwaste.obj")
nuclearWaste.AddTexture("textures/nuclearwaste.bmp")
nuclearWaste.translation.z = -5
nuclearWaste.scale.x = 0.7
nuclearWaste.scale.y = 0.7
nuclearWaste.scale.z = 0.7
nuclearWaste.translation.y = 0.09
nuclearWaste.translation.x = 4
rend.scene.append(nuclearWaste)

nuclearWaste = Model("models/nuclearwaste.obj")
nuclearWaste.AddTexture("textures/nuclearwaste.bmp")
nuclearWaste.translation.z = -3
nuclearWaste.scale.x = 0.7
nuclearWaste.scale.y = 0.7
nuclearWaste.scale.z = 0.7
nuclearWaste.translation.y = 0.5
nuclearWaste.translation.x = 4
nuclearWaste.rotation.x += 90
rend.scene.append(nuclearWaste)

nuclearWaste = Model("models/nuclearwaste.obj")
nuclearWaste.AddTexture("textures/nuclearwaste.bmp")
nuclearWaste.translation.z = -3
nuclearWaste.scale.x = 0.7
nuclearWaste.scale.y = 0.7
nuclearWaste.scale.z = 0.7
nuclearWaste.translation.y = 0.5
nuclearWaste.translation.x = -1
nuclearWaste.rotation.x += 90
nuclearWaste.rotation.z += 90
rend.scene.append(nuclearWaste)

stormtrooper = Model("models/stormtrooper.obj")
stormtrooper.AddTexture("textures/stormtrooper.bmp")
stormtrooper.translation.z = -5 + 5
stormtrooper.scale.x = 0.7
stormtrooper.scale.y = 0.7
stormtrooper.scale.z = 0.7
stormtrooper.translation.y = 0.09
stormtrooper.translation.x = 5
rend.scene.append(stormtrooper)

stormtrooper = Model("models/stormtrooper.obj")
stormtrooper.AddTexture("textures/stormtrooper.bmp")
stormtrooper.translation.z = -5 -2
stormtrooper.scale.x = 0.7
stormtrooper.scale.y = 0.7
stormtrooper.scale.z = 0.7
stormtrooper.translation.y = 0.09
stormtrooper.translation.x = 5
rend.scene.append(stormtrooper)

stormtrooper2 = Model("models/stormtrooper.obj")
stormtrooper2.AddTexture("textures/stormtrooper.bmp")
stormtrooper2.translation.z = -5 + 5
stormtrooper2.scale.x = 0.7
stormtrooper2.scale.y = 0.7
stormtrooper2.scale.z = 0.7
stormtrooper2.translation.y = 0.09
stormtrooper2.translation.x = -2
rend.scene.append(stormtrooper2)

stormtrooper2 = Model("models/stormtrooper.obj")
stormtrooper2.AddTexture("textures/stormtrooper.bmp")
stormtrooper2.translation.z = -5 - 2
stormtrooper2.scale.x = 0.7
stormtrooper2.scale.y = 0.7
stormtrooper2.scale.z = 0.7
stormtrooper2.translation.y = 0.09
stormtrooper2.translation.x = -2
rend.scene.append(stormtrooper2)



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
        snowGround.rotation.y -= 40 * deltaTime
        
    if keys[K_RIGHT]:
        snowGround.rotation.y += 40 * deltaTime
        
    if keys[K_UP]:
        camVerticalAngle += 30 * deltaTime  


    if keys[K_DOWN]:
        camVerticalAngle -= 30 * deltaTime
    
            
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
        camAngle -= 30 * deltaTime
        
    if keys[K_d]:
        camAngle += 30 * deltaTime
    
    if keys[K_w]:
        camDistance -= 3 * deltaTime
        if camDistance < minCamDistance:
            camDistance = minCamDistance
    
    if keys[K_s]:
        camDistance += 3 * deltaTime
        if camDistance > maxCamDistance:
            camDistance = maxCamDistance
        
    rend.time += deltaTime
    
    rend.camera.LookAt(snowGround.translation)
    rend.camera.Orbit(snowGround.translation, camDistance, camAngle, camVerticalAngle)
    
    # rend.camera.LookAt(faceModel.translation)
    
    rend.Render()
    pygame.display.flip()
    
pygame.quit()

#skeleton