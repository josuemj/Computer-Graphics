

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

width = 512
height = 384

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt =  RendererRT(screen)
rt.envMap = Texture('textures/city.bmp')
rt.glClearColor(0.5, 0.0, 0.0 )
rt.glClear()

#materials
brick = Material(difuse=[1, 0.2, 0.2], spec=128, Ks=0.25)
grass = Material(difuse=[0.2, 1.0, 0.2], spec=64, Ks=0.2)
mirror = Material(difuse=[0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bluemirror = Material(difuse=[0.5, 0.5, 1], spec = 128, Ks = 0.2, matType = REFLECTIVE)

marble = Material(texture=Texture('textures/whiteMarble.bmp'), spec=128, Ks = 0.2, matType=REFLECTIVE)

#materials
"""
Opaque
"""
earth = Material(ior=1.39, texture=Texture('textures/earth.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
neptune = Material(ior=1.33, texture=Texture('textures/neptune.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
"""
transparent
"""
glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)
bubble = Material(ior=1.5, texture=Texture('textures/bubble.bmp'), spec=128, Ks=0.2, matType=TRANSPARENT)
"""
Reflective
"""
sapphhire = Material(ior = 1.77, texture=Texture('textures/saphire.bmp'), spec=128, Ks=0.5, matType=REFLECTIVE)
ruby = Material(ior=1.76, texture=Texture('textures/ruby.bmp'), spec=128, Ks=0.5, matType=REFLECTIVE)

#lights
rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )
# rt.lights.append( DirectionalLight(direction = [0.5, -0.5, -1], intensity = 0.8, color = [1,1,1] ))
rt.lights.append( AmbientLight(intensity=0.1))

#Spheres
"""
Reflective
"""
rt.scene.append(Sphere(position=[2, 1, -5], radius=0.75, material=ruby))
rt.scene.append( Sphere(position = [2, -1, -5], radius = 0.75, material = sapphhire) ) #reflective saphire

"""
opaque
"""
rt.scene.append( Sphere(position = [-2, -1, -5], radius = 0.75, material = earth) ) # opaque earth 
rt.scene.append( Sphere(position = [-2, 1, -5], radius = 0.75, material = neptune) ) #opaque netune

"""
transparent
"""
rt.scene.append( Sphere(position = [0, 1 , -5], radius = 0.75, material = glass) ) #transparent bubble
rt.scene.append( Sphere(position = [0, -1 , -5], radius = 0.75, material = bubble) ) #transparent bubble



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