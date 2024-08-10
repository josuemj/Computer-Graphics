
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader, fragmentShader

width = 512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader


# puntoA = [50, 50, 0]
# puntoB = [250, 500, 0]
# puntoC = [500, 50, 0]

modelo1 = Model('models/model.obj')
modelo1.loadTexture('textures/model.bmp')
modelo1.translate[2] = -5

modelo1.scale[0] = 2
modelo1.scale[1] = 2
modelo1.scale[2] = 2


rend.models.append(modelo1)

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
