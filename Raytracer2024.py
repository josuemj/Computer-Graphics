

import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

width = 320
height = 240

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

# rt.lights.append( DirectionalLight(direction = [-1, -1, -1], intensity = 0.8) )
# # rt.lights.append( DirectionalLight(direction = [0.5, -0.5, -1], intensity = 0.8, color = [1,1,1] ))
# rt.lights.append( AmbientLight(intensity=0.1))

# rt.lights = []  # Reinicia las luces
rt.lights.append(DirectionalLight(direction=[1, -1, -1], intensity=1))  # Luz direccional más fuerte y en otro ángulo
rt.lights.append(AmbientLight(intensity=0.9))  # Aumenta la luz ambiental
# rt.lights.append(DirectionalLight(direction=[0.5, -0.5, -1], intensity=0.5))  


# rt.scene.append( Sphere(position = [0, 0 , -5], radius = 1, material = brick) )
# rt.scene.append( Sphere(position = [1, 1 , -3], radius = 0.5, material = earth) )

#planes
# rt.scene.append( Plane(position=[0,-5,-5], normal= [0,1,0], material=brick))

#disk
# rt.scene.append( Disk(position=[0, -1, -5], normal = [0, 1, 0], radius=1.5, material=mirror))

#cubes
# rt.scene.append( AABB(position = [1.5,1.5,-5], sizes = [1,1,1], material = brick))
# rt.scene.append( AABB(position = [-1.5,1.5,-5], sizes = [1,1,1], material = mirror))
# rt.scene.append( AABB(position = [1.5,-1.5,-5], sizes = [1,1,1], material = woodenBox))
# rt.scene.append( AABB(position = [-1.5,-1.5,-5], sizes = [1,1,1], material = glass))

#wall materials
# Definir materiales con colores más claros
white_floor_material = Material(difuse=[1.0, 1.0, 1.0], spec=1.5, Ks=0.1, )  # Blanco más brillante
red_material = Material(difuse=[1.0, 0.5, 0.5], spec=1.5, Ks=0.1, )  # Rojo claro
green_material = Material(difuse=[0.5, 1.0, 0.5], spec=1.5, Ks=0.1,  )  # Verde claro
blue_material = Material(difuse=[0.5, 0.5, 1.0], spec=1.5, Ks=0.1,  )  # Azul claro
yellow_material = Material(difuse=[1.0, 1.0, 0.5], spec=1.5, Ks=0.1  )  # Amarillo claro
cyan_material = Material(difuse=[0.5, 1.0, 1.0], spec=1.5, Ks=0.1)  # Cian claro

floor = Plane(position=[0, -2, 0], normal=[0, 1, 0], material=white_floor_material)


right_wall = Plane(position=[4, 0, 0], normal=[-1, 0, 0], material=brick)

# Pared Izquierda: Normal apuntando hacia la derecha (1 en el eje X)
left_wall = Plane(position=[-4, 0, 0], normal=[1, 0, 0], material=green_material)

# Pared del Fondo: Normal apuntando hacia la cámara o hacia adelante (1 en el eje Z)
back_wall = Plane(position=[0, 0, -10], normal=[0, 0, 1], material=blue_material)
ceiling = Plane(position=[0, 4, 0], normal=[0, -1, 0], material=cyan_material)

# Añadimos las paredes a la escena
rt.scene.append(right_wall)
rt.scene.append(left_wall)
rt.scene.append(back_wall)
rt.scene.append(floor)
rt.scene.append(ceiling)
rt.scene.append( Disk(position=[1.5, -1.9, -7], normal = [0, 1, 0], radius=1.5, material=brick))
rt.scene.append( AABB(position = [-1.2,-1.1,-4], sizes = [1,1,1], material = brick))
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