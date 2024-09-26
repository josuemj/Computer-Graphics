

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

width = 128
height = 96

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt =  RendererRT(screen)
rt.envMap = Texture('textures/parkingLot.bmp')
rt.glClearColor(0.5, 0.0, 0.0 )
rt.glClear()

brick = Material(difuse=[1, 0.2, 0.2], spec=128, Ks=0.25)
grass = Material(difuse=[0.2, 1.0, 0.2], spec=64, Ks=0.2)
mirror = Material(difuse=[0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bluemirror = Material(difuse=[0.5, 0.5, 1], spec = 128, Ks = 0.2, matType = REFLECTIVE)

earth = Material(texture=Texture('textures/earth.bmp'))
marble = Material(texture=Texture('textures/whiteMarble.bmp'), spec=128, Ks = 0.2, matType=REFLECTIVE)
glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)

 

rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )
# rt.lights.append( DirectionalLight(direction = [0.5, -0.5, -1], intensity = 0.8, color = [1,1,1] ))
rt.lights.append( AmbientLight(intensity=0.1))


rt.scene.append( Sphere(position = [0, -1 , -5], radius = 0.75, material = glass) ) #transparent glass
rt.scene.append( Sphere(position = [2, -1, -5], radius = 0.75, material = glass) )  # reflective ruby
rt.scene.append( Sphere(position = [-2, -1, -5], radius = 0.75, material = glass) ) # opaque earth 
 
rt.scene.append( Sphere(position = [0, 1 , -5], radius = 0.75, material = glass) ) #transparent bubble
rt.scene.append( Sphere(position = [2, 1, -5], radius = 0.75, material = glass) ) #reflective saphire
rt.scene.append( Sphere(position = [-2, 1, -5], radius = 0.75, material = glass) ) #opaque netune


# rt.scene.append( Sphere(position = [-2, -1 , -5], radius = 1, material = glass) )
# rt.scene.append( Sphere(position = [2, 0 , -5], radius = 1, material = glass) )

# rt.scene.append( Sphere(position = [2, 1 , -5], radius = 1, material = glass) )







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