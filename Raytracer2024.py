import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

width = 256
height = 256

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
metal = Material(difuse=[0.8, 0.8, 0.8], spec=128, Ks=0.3, matType=OPAQUE)

# earth = Material(texture=Texture('textures/earth.bmp'))
# marble = Material(texture=Texture('textures/whiteMarble.bmp'), spec=128, Ks = 0.2, matType=REFLECTIVE)
# glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)

# woodenBox = Material( texture=Texture("textures/woodenBox.bmp"))

# rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )
# rt.lights.append( DirectionalLight(direction = [0.5, -0.5, -1], intensity = 0.8, color = [1,1,1] ))
rt.lights.append( AmbientLight(intensity=1))


cylinder = Cylinder(position=[0, 0, -5], radius=1, height=3, material=metal)
rt.scene.append(cylinder)

v0 = [-1, 0, -3]
v1 = [1, 0, -3]
v2 = [0, 1.5, -3]
triangle = Triangle(v0, v1, v2, material=grass)
rt.scene.append(triangle)


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