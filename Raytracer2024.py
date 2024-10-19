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

"""
LIGHTS
"""
# Add an Ambient Light
rt.lights.append(AmbientLight(intensity=0.5))

# Adjust the Directional Light to better illuminate the pyramid
rt.lights.append(DirectionalLight(direction=[-1, -1, -1], intensity=0.7))

# Add a Point Light near the pyramid to highlight its faces
rt.lights.append(PointLight(color=[1, 1, 1], intensity=1.0, position=[0, 2, -4]  ))

"""
PYRAMIDS
"""

pyramid = Pyramid( #BLUE MIRROR BIG ONE tallest on row
    base_center=[-7, -4, -40],  
    base_size=7,              # Base size of the pyramid
    height=12,                 # Height of the pyramid
    material=bluemirror,
    pitch=0,
    yaw=50,
    roll=0
)
rt.scene.append(pyramid)

pyramid2 = Pyramid( #MIDDLE RED ONE on row
    base_center=[-1, -4, -20], 
    base_size=4,              
    height=4,                 
    material=redMirror,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid2)

pyramid3 = Pyramid( #RIGHT TO THE RED MIRROR PYRAMID
    base_center=[3, -4, -30],  
    base_size=3,              
    height=6,                 
    material=mirror,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid3)

pyramid4 = Pyramid( #MIDDLE ON ROW
    base_center=[-7, -4, -25],
    base_size=3.5,              
    height=4,                 
    material=metallicMaterial,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid4)



pyramid5 = Pyramid( #SMALLEST ON LINE LEFT
    base_center=[-6.5, -4, -17],  
    base_size=2,              
    height=1.5,                
    material=grass,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid5)

pyramid6 = Pyramid( #RIGHT ONE BIG UNIQUE ISOLATED
    base_center=[6, -4, -15],  
    base_size=3,              
    height=3,                 
    material=metallicMaterial,
    pitch=0,
    yaw=45,
    roll=0
)
rt.scene.append(pyramid6)

"""
CYLINDERS
"""
cylinder1 = Cylinder( #LEFT CYLINDER
    position=[-14, -4+(12/2), -45],   
    radius=3,              
    height=12,               
    material=metallicMaterial 
)
rt.scene.append(cylinder1)


cylinder2 = Cylinder( #RIGHT CYLINDER
    position=[21, -4+(16/2), -45],    
    radius=2,              
    height=16,                
    material=metallicMaterial 
)
rt.scene.append(cylinder2)

"""
TOROIDS
"""
torus = Torus( #ISOLATED TORUS
    position=[-3, 3, -8],           # Center of the torus
    major_radius=1,               # Major radius (distance from center to tube center)
    minor_radius=0.3,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=0,                          
    yaw=-20,                        
    roll=10                        
)
rt.scene.append(torus)

torus2 = Torus( # (FIRST) FIRST BLUE MIRROR 
    position=[0.5, 5, -50],           # Center of the torus
    major_radius=7,               # Major radius (distance from center to tube center)
    minor_radius=1,              # Minor radius (radius of the tube)
    material=bluemirror,
    pitch=75,                      # Rotate around the X-axis    
    yaw=-0,                        # Rotate around the Y-axis
    roll=0                        # Rotate around the Z-axis
)
rt.scene.append(torus2)

torus3 = Torus( # (SECOND) WHITE
    position=[0.5, 10, -50],                          
    minor_radius=1,              
    material=white_floor_material,
    pitch=75,                          
    yaw=-0,                       
    roll=0                        
)
rt.scene.append(torus3)

torus4 = Torus( # (THIRD) ORANGE
    position=[0.6, 14, -50],          
    major_radius=5,               
    minor_radius=1,              
    material=orange_material,
    pitch=75,                         
    yaw=-0,                        
    roll=-7                        
)
rt.scene.append(torus4) 

torus5 = Torus( # (FOURTH) BLUE MIRROR
    position=[0.7, 18, -50],          
    major_radius=4,               
    minor_radius=1,              
    material=bluemirror,
    pitch=75,                      
    yaw=-0,                    
    roll=-15                     
)
rt.scene.append(torus5) 

torus6 = Torus( # (FIFTH) WHITE
    position=[0.8, 22, -50],     
    major_radius=3,               
    minor_radius=0.8,              
    material=white_floor_material,
    pitch=75,                          
    yaw=-0,                       
    roll=-15                     
)
rt.scene.append(torus6) 

torus7 = Torus( # (LAST SMALLEST) ONE
    position=[1.3, 26, -50],         
    major_radius=1,               
    minor_radius=0.4,             
    material=orange_material,
    pitch=75,                         
    yaw=-0,                       
    roll=-15                     
)
rt.scene.append(torus7) 

"""
PLANE
"""
floor = Plane(position=[0, -4, 0], normal=[0, 1, 0], material=bluemirror)
rt.scene.append(floor)

"""
BOXES
"""
box = Box( #GREE ONE TALLEST
    position=[0.5, -4+(18/2), -50],     # Position of the box (base center at y = -1)
    sizes=[4, 18, 5],          # Width, height, depth
    material=grass, 
    pitch=0,                 
    yaw=45,                   
    roll=0                    
)
rt.scene.append(box)

box2 = Box(#LEEFT ONE ORANGE
    position=[-13, -4+(3/2), -28],    
    sizes=[3, 3, 3],          
    material=orange_material, 
    pitch=0,
    yaw=60,                   
    roll=0                    
)
rt.scene.append(box2)

box3 = Box(#SMALL ONE RIGHT - ORANGE
    position=[2.3, -4+(1.3/2), -12],     
    sizes=[1.3, 1.3, 1.3],          
    material=orange_material, 
    pitch=0,
    yaw=30,          
    roll=0            
)
rt.scene.append(box3)

box4 = Box( #RED MIRROR RIGHT BOTTOM LEFT
    position=[-4.5, -4+(1/2), -10],     
    sizes=[1, 1, 1],          
    material=redMirror, 
    pitch=0,
    yaw=60,   
    roll=0     
)
rt.scene.append(box4)

"""
SPHERES
"""
sphere1 = Sphere(# big one cheese biggest one MIDDLE
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

sphere3 = Sphere( #middle white between pizza and cheese
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