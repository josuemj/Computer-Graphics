import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

width = 512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt =  RendererRT(screen)
rt.envMap = Texture('textures/parkingLot.bmp')
rt.glClearColor(0.5, 0.0, 0.0 )
rt.glClear()

#materials
brick = Material(difuse=[1, 0.2, 0.2], spec=128, Ks=0.25)
grass = Material(difuse=[0.2, 1.0, 0.2], spec=64, Ks=0.2)
mirror = Material(difuse=[0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bluemirror = Material(difuse=[0.5, 0.5, 1], spec = 128, Ks = 0.2, matType = REFLECTIVE)
glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)
cheese = Material(texture=Texture('textures/cheese.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
pizza = Material(texture=Texture('textures/pizza.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
redMirror = Material(texture=Texture("textures/mirror.bmp"), difuse=[1, 0, 0], spec = 128, Ks = 0.2, matType = REFLECTIVE)
# earth = Material(texture=Texture('textures/earth.bmp'))
# marble = Material(texture=Texture('textures/whiteMarble.bmp'), spec=128, Ks = 0.2, matType=REFLECTIVE)
# woodenBox = Material( texture=Texture("textures/woodenBox.bmp"))

#lights
# Add an Ambient Light
rt.lights.append(AmbientLight(intensity=0.5))

# Adjust the Directional Light to better illuminate the pyramid
rt.lights.append(DirectionalLight(
    direction=[-1, -1, -1],  # Adjust the direction as needed
    intensity=0.7
))

# Add a Point Light near the pyramid to highlight its faces
rt.lights.append(PointLight(
    color=[1, 1, 1],
    intensity=1.0,
    position=[0, 2, -4]  # Position it above the pyramid
))


pyramid = Pyramid(
    base_center=[0, 0, -4],
    base_size=1,
    height=2,
    material=bluemirror,
    pitch=30,  # Rotate 30 degrees around the X-axis
    yaw=45,    # Rotate 45 degrees around the Y-axis
    roll=0     # No rotation around the Z-axis
)

# rt.scene.append(pyramid)

# Assuming you have a material instance called 'metal'

torus = Torus(
    position=[-2.4, 2.3, -8],           # Center of the torus
    major_radius=1,               # Major radius (distance from center to tube center)
    minor_radius=0.3,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=0,                      # Rotate 30 degrees around the X-axis    
    yaw=-20,                        # Rotate 45 degrees around the Y-axis
    roll=10                        # Rotate 60 degrees around the Z-axis
)

# Add the torus to your scene
rt.scene.append(torus)


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