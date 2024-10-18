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
white_floor_material = Material(difuse=[1.0, 1.0, 1.0], spec=1.5, Ks=0.1, )  # Blanco más brillante
metallicMaterial = Material(
difuse=[0.8, 0.8, 0.8],  
    spec=256,                 
    Ks=0.5,                   
    matType=REFLECTIVE       
)

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


pyramid = Pyramid( #big one leftr
    base_center=[-7, -4, -40],  # Positioned higher to ensure visibility and reflection
    base_size=7,              # Base size of the pyramid
    height=12,                 # Height of the pyramid
    material=bluemirror,
    pitch=0,
    yaw=50,
    roll=0
)
rt.scene.append(pyramid)

pyramid2 = Pyramid( #MIDDLE RED ONE
    base_center=[-1, -4, -20],  # Positioned higher to ensure visibility and reflection
    base_size=4,              # Base size of the pyramid
    height=4,                 # Height of the pyramid
    material=redMirror,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid2)

pyramid3 = Pyramid( #big one leftr
    base_center=[3, -4, -30],  # Positioned higher to ensure visibility and reflection
    base_size=3,              # Base size of the pyramid
    height=6,                 # Height of the pyramid
    material=mirror,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid3)

pyramid4 = Pyramid( #MIDDLE ON LINE
    base_center=[-7, -4, -25],  # Positioned higher to ensure visibility and reflection
    base_size=3.5,              # Base size of the pyramid
    height=4,                 # Height of the pyramid
    material=metallicMaterial,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid4)



pyramid5 = Pyramid( #small one on line
    base_center=[-6.5, -4, -17],  # Positioned higher to ensure visibility and reflection
    base_size=2,              # Base size of the pyramid
    height=1.5,                 # Height of the pyramid
    material=grass,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid5)

cylinder1 = Cylinder(
    position=[-14, -4+(12/2), -45],   # Position of the first cylinder
    radius=3,              # Radius of the cylinder
    height=12,                # Height of the cylinder
    material=metallicMaterial # Use the metallic material
)
rt.scene.append(cylinder1)


# Create the second cylinder
cylinder2 = Cylinder(
    position=[21, -4+(16/2), -45],    # Position of the second cylinder (to the right)
    radius=2,              # Radius of the cylinder
    height=16,                # Height of the cylinder
    material=metallicMaterial # Use the metallic material
)
rt.scene.append(cylinder2)


torus = Torus(
    position=[-3, 3, -8],           # Center of the torus
    major_radius=1,               # Major radius (distance from center to tube center)
    minor_radius=0.3,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=0,                      # Rotate 30 degrees around the X-axis    
    yaw=-20,                        # Rotate 45 degrees around the Y-axis
    roll=10                        # Rotate 60 degrees around the Z-axis
)
# Add the torus to your scene
rt.scene.append(torus)

floor = Plane(position=[0, -4, 0], normal=[0, 1, 0], material=bluemirror)
rt.scene.append(floor)



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