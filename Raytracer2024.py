

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import Material
from lights import *


width =  512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt =  RendererRT(screen)

brick = Material(difuse=[1, 0.2, 0.2], spec=128, Ks=0.25)
grass = Material(difuse=[0.2, 1.0, 0.2], spec=64, Ks=0.2)

snowy = Material(
    difuse=[0.95, 0.95, 0.95],
    spec=128,
    Ks=0.3
)

button = Material(
    difuse=[0.09, 0.09, 0.09],  # Very dark grey, nearly black
    spec=32,                  # Lower specular exponent for a softer highlight
    Ks=0.1                        # Low specular coefficient for a matte finish
)

orange_carrot = Material(
    difuse = [1.0, 0.5, 0.0], 
    spec = 32,              
    Ks = 0.2                    
)

rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )
rt.lights.append( DirectionalLight(direction = [0.5, -0.5, -1], intensity = 0.8, color = [1,1,1] ))
rt.lights.append( AmbientLight(intensity=0.1))

rt.scene.append( Sphere(position=[0, 0.6, -2.8], radius=0.3, material=snowy)) #head ball
rt.scene.append( Sphere(position=[0, 0.5, -2.55], radius=0.06, material=orange_carrot)) # nose
rt.scene.append( Sphere(position=[-0.04, 0.44, -2.57], radius=0.025, material=button)) # mouth
rt.scene.append( Sphere(position=[0.04, 0.44, -2.57], radius=0.025, material=button)) # mouth
rt.scene.append( Sphere(position=[0.11, 0.46, -2.58], radius=0.025, material=button)) # mouth
rt.scene.append( Sphere(position=[-0.11, 0.46, -2.58], radius=0.025, material=button)) # mouth

rt.scene.append( Sphere(position=[-0.09, 0.6, -2.52], radius=0.03, material=button)) # eye
rt.scene.append( Sphere(position=[0.09, 0.6, -2.52], radius=0.03, material=button)) # eye


rt.scene.append( Sphere(position=[0, 0, -2.9], radius=0.4, material=snowy)) # middle ball
rt.scene.append( Sphere(position=[0, 0.25, -2.58], radius=0.04, material=button)) # top button
rt.scene.append( Sphere(position=[0, 0, -2.53], radius=0.05, material=button)) # middle button


rt.scene.append( Sphere(position=[0, -0.7, -3], radius=0.5, material=snowy)) #bottom snowbal
rt.scene.append( Sphere(position=[0, -0.5, -2.6], radius=0.09, material=button)) #bottom buttom



rt.glRender()

isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
	
				
	pygame.display.flip()
	clock.tick(60)
	
pygame.quit()