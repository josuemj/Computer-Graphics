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
"""
COLORS
"""
brick = Material(difuse=[1, 0.2, 0.2], spec=128, Ks=0.25)
grass = Material(difuse=[0.2, 1.0, 0.2], spec=64, Ks=0.2)
white_floor_material = Material(difuse=[1.0, 1.0, 1.0], spec=1.5, Ks=0.1, )  # Blanco más brillante

"""
REFLECTIVE
"""
redMirror = Material(texture=Texture("textures/mirror.bmp"), difuse=[1, 0, 0], spec = 128, Ks = 0.2, matType = REFLECTIVE)
mirror = Material(difuse=[0.9, 0.9, 0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bluemirror = Material(difuse=[0.5, 0.5, 1], spec = 128, Ks = 0.2, matType = REFLECTIVE)
metallicMaterial = Material(difuse=[0.8, 0.8, 0.8], spec=256, Ks=0.5, matType=REFLECTIVE)

"""
OPAQUE
"""
cheese = Material(texture=Texture('textures/cheese.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
pizza = Material(texture=Texture('textures/pizza.bmp'), spec=128, Ks=0.2, matType=OPAQUE) 
orange_material = Material(difuse=[1.0, 0.5, 0.0], spec=128, Ks=0.25, matType=OPAQUE)

"""
TRANSPARENT
"""
glass = Material(ior = 1.5, spec = 128, Ks = 0.2, matType=TRANSPARENT)
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

#PYRAMIDS

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

pyramid3 = Pyramid( #big one right
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

pyramid6 = Pyramid( #RIGHT ONE
    base_center=[6, -4, -15],  # Positioned higher to ensure visibility and reflection
    base_size=3,              # Base size of the pyramid
    height=3,                 # Height of the pyramid
    material=metallicMaterial,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid6)

# CYLINDERS

cylinder1 = Cylinder( #left one
    position=[-14, -4+(12/2), -45],   # Position of the first cylinder
    radius=3,              # Radius of the cylinder
    height=12,                # Height of the cylinder
    material=metallicMaterial # Use the metallic material
)
rt.scene.append(cylinder1)


# right one
cylinder2 = Cylinder(
    position=[21, -4+(16/2), -45],    # Position of the second cylinder (to the right)
    radius=2,              # Radius of the cylinder
    height=16,                # Height of the cylinder
    material=metallicMaterial # Use the metallic material
)
rt.scene.append(cylinder2)

#TORUS left one
torus = Torus(
    position=[-3, 3, -8],           # Center of the torus
    major_radius=1,               # Major radius (distance from center to tube center)
    minor_radius=0.3,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=0,                      # Rotate 30 degrees around the X-axis    
    yaw=-20,                        # Rotate 45 degrees around the Y-axis
    roll=10                        # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus)

torus2 = Torus( # first on stack
    position=[0.5, 5, -50],           # Center of the torus
    major_radius=7,               # Major radius (distance from center to tube center)
    minor_radius=1,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=75,                      # Rotate 30 degrees around the X-axis    
    yaw=-0,                        # Rotate 45 degrees around the Y-axis
    roll=0                        # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus2)

torus3 = Torus(
    position=[0.5, 10, -50],           # Center of the torus
    major_radius=6,               # Major radius (distance from center to tube center)
    minor_radius=1,              # Minor radius (radius of the tube)
    material=white_floor_material,
    pitch=75,                      # Rotate 30 degrees around the X-axis    
    yaw=-0,                        # Rotate 45 degrees around the Y-axis
    roll=0                        # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus3)

torus4 = Torus(
    position=[0.6, 14, -50],           # Center of the torus
    major_radius=5,               # Major radius (distance from center to tube center)
    minor_radius=1,              # Minor radius (radius of the tube)
    material=orange_material,
    pitch=75,                      # Rotate 30 degrees around the X-axis    
    yaw=-0,                        # Rotate 45 degrees around the Y-axis
    roll=-7                        # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus4) 

torus5 = Torus(
    position=[0.7, 18, -50],           # Center of the torus
    major_radius=4,               # Major radius (distance from center to tube center)
    minor_radius=1,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=75,                      # Rotate 30 degrees around the X-axis    
    yaw=-0,                        # Rotate 45 degrees around the Y-axis
    roll=-15                      # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus5) 

torus6 = Torus(
    position=[0.8, 22, -50],           # Center of the torus
    major_radius=3,               # Major radius (distance from center to tube center)
    minor_radius=0.8,              # Minor radius (radius of the tube)
    material=white_floor_material,
    pitch=75,                      # Rotate 30 degrees around the X-axis    
    yaw=-0,                        # Rotate 45 degrees around the Y-axis
    roll=-15                      # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus6) 

torus7 = Torus(
    position=[1.3, 26, -50],           # Center of the torus
    major_radius=1,               # Major radius (distance from center to tube center)
    minor_radius=0.4,              # Minor radius (radius of the tube)
    material=orange_material,
    pitch=75,                      # Rotate 30 degrees around the X-axis    
    yaw=-0,                        # Rotate 45 degrees around the Y-axis
    roll=-15                      # Rotate 60 degrees around the Z-axis
)
rt.scene.append(torus7) 

#PLANE
floor = Plane(position=[0, -4, 0], normal=[0, 1, 0], material=bluemirror)
rt.scene.append(floor)

#BOXES
box = Box( #GREE ONE TALLEST
    position=[0.5, -4+(18/2), -50],     # Position of the box (base center at y = -1)
    sizes=[4, 18, 5],          # Width, height, depth
    material=grass, # Use the metallic material
    pitch=0,                 # Rotate around the X-axis
    yaw=45,                   # Rotate around the Y-axis
    roll=0                    # No rotation around the Z-axis
)
rt.scene.append(box)

box2 = Box(#LEFT ONE
    position=[-13, -4+(3/2), -28],     # Position of the box (base center at y = -1)
    sizes=[3, 3, 3],          # Width, height, depth
    material=orange_material, # Use the metallic material
    pitch=0,# Rotate around the X-axis
    yaw=60,                   # Rotate around the Y-axis
    roll=0                    # No rotation around the Z-axis
)
rt.scene.append(box2)

box3 = Box(#SMALL ONE RIGHT
    position=[2.3, -4+(1.3/2), -12],     # Position of the box (base center at y = -1)
    sizes=[1.3, 1.3, 1.3],          # Width, height, depth
    material=orange_material, # Use the metallic material
    pitch=0,# Rotate around the X-axis
    yaw=30,                   # Rotate around the Y-axis
    roll=0                    # No rotation around the Z-axis
)
rt.scene.append(box3)

box4 = Box(
    position=[-4.5, -4+(1/2), -10],     # Position of the box (base center at y = -1)
    sizes=[1, 1, 1],          # Width, height, depth
    material=redMirror, # Use the metallic material
    pitch=0,# Rotate around the X-axis
    yaw=60,                   # Rotate around the Y-axis
    roll=0                    # No rotation around the Z-axis
)
rt.scene.append(box4)

# SPHERES
sphere1 = Sphere(# big one cheese biggest one
    position = [0, -4+0.8 , -9], 
    radius = 0.8, 
    material = cheese
    )
rt.scene.append(sphere1)

sphere2 = Sphere( #small bottom pizza
    position = [-2.6, -4+0.4 , -8], 
    radius = 0.4, 
    material = pizza
    )
rt.scene.append(sphere2)

sphere3 = Sphere(
    position = [-2.4, -4+1 , -11], 
    radius = 1, 
    material = white_floor_material
    )
rt.scene.append(sphere3)

sphere4 = Sphere( # biigest one right cylinder
    position = [11, -4+4 , -40], 
    radius = 4, 
    material = white_floor_material
    )
rt.scene.append(sphere4)
    
sphere5 = Sphere( #smallest right
    position = [3.5, -4+0.4, -9], 
    radius = 0.4, 
    material = white_floor_material
    )
rt.scene.append(sphere5)

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