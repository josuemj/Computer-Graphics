
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import *

width = 1792
height = 1024

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.glLoadBackground('textures/garden.bmp')

modelo1 = Model('models/LionSculpture.obj')
modelo1.loadTexture('textures/ModelTexture.bmp')
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = vintageYellowShader
modelo1.translate[2] = -5
modelo1.translate[0] = 1.2
modelo1.translate[1] = -2.1
modelo1.scale[0] = 1.8
modelo1.scale[1] = 1.8 
modelo1.scale[2] = 1.8
modelo1.rotate[1] += 90

modelo2 = Model('models/dino.obj')
modelo2.loadTexture('textures/dino.bmp')
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = blueGrayShader
modelo2.translate[2] = -16
modelo2.translate[0] = -6
modelo2.translate[1] = 1.5
modelo2.scale[0] = 1.5
modelo2.scale[1] = 1.6
modelo2.scale[2] = 1.5
modelo2.rotate[0] -= 90
modelo2.rotate[2] += 70

modelo3 = Model('models/tartaruga.obj')
modelo3.loadTexture('textures/tartaruga.bmp')
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = woodShader
modelo3.translate[2] = -5
modelo3.translate[0] = -3.1
modelo3.translate[1] = -1.8
modelo3.scale[0] = 0.15
modelo3.scale[1] = 0.15
modelo3.scale[2] = 0.15
modelo3.rotate[0] -= 60
modelo3.rotate[1] += 10 #on this one rolls (like 6)
modelo3.rotate[2] -= 20

modelo4 = Model('models/rocket.obj')
modelo4.loadTexture('textures/rocket.bmp')
modelo4.vertexShader = vertexShader
modelo4.fragmentShader = missileShader
modelo4.translate[2] = -5
modelo4.translate[0] = 1.2
modelo4.translate[1] = 2
modelo4.scale[0] = 0.003
modelo4.scale[1] = 0.003
modelo4.scale[2] = 0.003
modelo4.rotate[1] -= 35
modelo4.rotate[0] += 30

rend.models.append(modelo2)
rend.models.append(modelo1)	
rend.models.append(modelo3)
rend.models.append(modelo4)


isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
			elif event.key == pygame.K_1:
				rend.primitiveType = POINTS
				
			elif event.key == pygame.K_2:
				rend.primitiveType = LINES
				
			elif event.key == pygame.K_3:
				rend.primitiveType = TRIANGLES
			
			elif event.key == pygame.K_4: #pitch (x)
				modelo1.rotate[0] += 5			
			elif event.key == pygame.K_5:# Yaw (y)
				modelo1.rotate[1] += 5
			elif event.key == pygame.K_6:# pitch (z)
				modelo1.rotate[2] += 5
				
			elif event.key == pygame.K_RIGHT:
				rend.camera.translate[0] += 1
			elif event.key == pygame.K_LEFT:
				rend.camera.translate[0] -= 1
			elif event.key == pygame.K_UP:
				rend.camera.translate[1] += 1
			elif event.key == pygame.K_DOWN:
				rend.camera.translate[1] -= 1
				
					
	rend.glClear()
	rend.glClearBackground()
	
	rend.glRender()
	#rend.glTriangle(puntoA, puntoB, puntoC)

	pygame.display.flip()
	clock.tick(60)
	
rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
