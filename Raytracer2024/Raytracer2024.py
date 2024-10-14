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

earth = Material(texture=Texture('textures/earth.bmp'))
marble = Material(texture=Texture('textures/whiteMarble.bmp'), spec=128, Ks = 0.2, matType=REFLECTIVE)
glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)

# woodenBox = Material( texture=Texture("textures/woodenBox.bmp"))

# rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )


cheese = Material(texture=Texture('textures/cheese.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
pizza = Material(texture=Texture('textures/pizza.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
redMirror = Material(texture=Texture("textures/mirror.bmp"), difuse=[1, 0, 0], spec = 128, Ks = 0.2, matType = REFLECTIVE)

# woodenBox = Material( texture=Texture("textures/woodenBox.bmp"))

# rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )
# rt.lights.append( DirectionalLight(direction = [0.5, -0.5, -1], intensity = 0.8, color = [1,1,1] ))
rt.lights.append( AmbientLight(intensity=1))


cylinder = Cylinder(position=[-1, -1, -4], radius=0.6, height=0.7, material=cheese)
rt.scene.append(cylinder)

cylinder2 = Cylinder(position=[1.2, -1, -5], radius=1, height=1, material=glass)
rt.scene.append(cylinder2)

cylinder3 = Cylinder(position=[1.2, 0, -5], radius=0.5, height=1, material=bluemirror)
rt.scene.append(cylinder3)

v0 = [-3, 1, -7]
v1 = [-1, 1, -7]
v2 = [-2, 2.5, -8]
triangle = Triangle(v0, v1, v2, material=glass)
rt.scene.append(triangle) 


v3 = [3, 2, -9]
v4 = [1.2, 2, -8]
v5 = [2, 4, -8]
triangle2 = Triangle(v3, v4, v5, material=pizza)
rt.scene.append(triangle2) 

v0 = [-2, -1.5, -3]  
v1 = [1, -1.5, -3]   
v2 = [-2, -1.5, -6] 
triangle3 = Triangle(v0, v1, v2, material=redMirror)
rt.scene.append(triangle3) 
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