

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

width = 32
height = 32

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt =  RendererRT(screen)
# rt.envMap = Texture('textures/parkingLot.bmp')
rt.glClearColor(1,0, 0)
rt.glClear()

brick = Material(difuse=[1, 0.2, 0.2], spec=128, Ks=0.25)
grass = Material(difuse=[0.2, 1.0, 0.2], spec=64, Ks=0.2)
mirror = Material(difuse=[0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bluemirror = Material(difuse=[0.5, 0.5, 1], spec = 128, Ks = 0.2, matType = REFLECTIVE)

earth = Material(texture=Texture('textures/earth.bmp'))
marble = Material(texture=Texture('textures/whiteMarble.bmp'), spec=128, Ks = 0.2, matType=REFLECTIVE)
glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)
woodenBox = Material( texture=Texture("textures/woodenBox.bmp"))
tnt = Material( texture=Texture("textures/tnt.bmp"))

rt.lights.append(DirectionalLight(direction=[1, -1, -1], intensity=1))  # Luz direccional más fuerte y en otro ángulo
rt.lights.append(AmbientLight(intensity=1))  # Aumenta la luz ambiental


#wall materials
white_floor_material = Material(difuse=[1.0, 1.0, 1.0], spec=1.5, Ks=0.1, )  # Blanco más brillante
red_material = Material(difuse=[1.0, 0.5, 0.5], spec=1.5, Ks=0.1, )  # Rojo claro
green_material = Material(difuse=[0.5, 1.0, 0.5], spec=1.5, Ks=0.1,  )  # Verde claro
blue_material = Material(difuse=[0.5, 0.5, 1.0], spec=1.5, Ks=0.1,  )  # Azul claro
yellow_material = Material(difuse=[1.0, 1.0, 0.5], spec=1.5, Ks=0.1  )  # Amarillo claro
cyan_material = Material(difuse=[0.5, 1.0, 1.0], spec=1.5, Ks=0.1)  # Cian claro
blue_dark_sea_material = Material(difuse=[0.0, 0.2, 0.5], spec=1.5, Ks=0.3)  
brown_material = Material(difuse=[0.4, 0.2, 0.1], spec=1.5, Ks=0.3)  
mustard_yellow_material = Material(difuse=[0.8, 0.7, 0.2], spec=1.5, Ks=0.3)  
light_lime_green_material = Material(difuse=[0.6, 1.0, 0.4], spec=1.5, Ks=0.3)  

#planes
floor = Plane(position=[0, -2, 0], normal=[0, 1, 0], material=white_floor_material)
right_wall = Plane(position=[4, 0, 0], normal=[-1, 0, 0], material=blue_dark_sea_material)
left_wall = Plane(position=[-4, 0, 0], normal=[1, 0, 0], material=light_lime_green_material )
back_wall = Plane(position=[0, 0, -10], normal=[0, 0, 1], material=mustard_yellow_material)
ceiling = Plane(position=[0, 4, 0], normal=[0, -1, 0], material=brown_material)

#scence addition
rt.scene.append(right_wall)
rt.scene.append(left_wall)
rt.scene.append(back_wall)
rt.scene.append(floor)
rt.scene.append(ceiling)
rt.scene.append( Disk(position=[1.5, -1.9, -7], normal = [0, 1, 0], radius=1.5, material=mirror))
rt.scene.append( AABB(position = [-1.2,-1.1,-4], sizes = [1,1,1], material = tnt))
rt.scene.append( AABB(position = [1.5,-1.5,-7], sizes = [1,1,1], material = woodenBox))


#Room planes
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