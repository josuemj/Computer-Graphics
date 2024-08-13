
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import *

width = 940
height = 540

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rend = Renderer(screen)

modelo1 = Model('models/base.obj')
modelo1.loadTexture('textures/hearth.bmp')
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = fragmentShader
modelo1.translate[2] = -5
modelo1.translate[0] = -2
modelo1.scale[0] = 1.5
modelo1.scale[1] = 1.5
modelo1.scale[2] = 1.5

modelo2 = Model('models/base.obj')
modelo2.loadTexture('textures/hearth.bmp')
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = fragmentShader
modelo2.translate[2] = -5
modelo2.translate[0] = 0
modelo2.scale[0] = 1.5
modelo2.scale[1] = 1.5
modelo2.scale[2] = 1.5

modelo3 = Model('models/base.obj')
modelo3.loadTexture('textures/hearth.bmp')
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = fragmentShader
modelo3.translate[2] = -5
modelo3.translate[0] = 2
modelo3.scale[0] = 1.5
modelo3.scale[1] = 1.5
modelo3.scale[2] = 1.5


rend.models.append(modelo1)
rend.models.append(modelo2)
rend.models.append(modelo3)


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
			
			elif event.key == pygame.K_4:
				modelo1.rotate[0] += 5			
			elif event.key == pygame.K_5:
				modelo1.rotate[1] += 5
			elif event.key == pygame.K_6:
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
	
	rend.glRender()
	#rend.glTriangle(puntoA, puntoB, puntoC)

	pygame.display.flip()
	clock.tick(60)
	
rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
