import numpy as np
from intercept import Intercept
from math import tan, pi, atan2, acos

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None

    
class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__( position, material)
        self.radius = radius
        self.type = "Sphere"
        
    def ray_intersect(self, orig, dir):
        L = np.subtract(self.position, orig)
        tca = np.dot(L,  dir)
        
        d = (np.linalg.norm(L) ** 2 - tca ** 2) ** 0.5
        
        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 < 0: 
            t0 = t1 
        if t0 < 0:
            return None
        
        # P = orig + dir * t0
        P = np.add(orig, np.multiply(dir, t0))
        normal = np.subtract(P, self.position)
        normal /= np.linalg.norm(      normal)
        
        u = (atan2(normal[2], normal[0]) / (2 * pi) + 0.5)
        v = acos(-normal[1]) / pi
        
        return Intercept(point = P, 
                         normal = normal,
                         distance = t0,
                         rayDirection=dir,
                         obj = self,
                         texCoords= [u, v]
                         )        

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normal
        self.type = "Plane"
        
    def ray_intersect(self, orig, dir):
        
        denom = np.dot(dir, self.normal)
        
        if abs(denom) < 0.0001:
            return None
        
        num = np.dot(np.subtract(self.position, orig), self.normal)
        
        t = num /denom
        
        if t < 0:
            return None
        
        P = np.add(orig, np.array(dir) * t)
        return Intercept(
            point=P,
            normal=self.normal,
            distance = t,
            texCoords= None,
            rayDirection=dir,
            obj=self
        )
    
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"
    
    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)
        
        if planeIntercept is None:
            return None
        
        contact = np.subtract(planeIntercept.point, self.position)
        contact = np.linalg.norm(contact)
        
        if contact > self.radius:
            return None
        
        return planeIntercept

class AABB(Shape):
    #Axis Aligned Bounding Box (cube)
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"
        
        self.planes = []
        
        rightPlane = Plane( [position[0] + sizes[0]/2, position[1], position[2]], [ 1,0,0], material)
        leftPlane = Plane( [position[0] - sizes[0]/2, position[1], position[2]], [-1,0,0], material)

        upPlane = Plane( [position[0], position[1] + sizes[1]/2, position[2]], [0, 1,0], material)
        downPlane = Plane( [position[0], position[1] - sizes[1]/2, position[2]], [0,-1,0], material)

        frontPlane = Plane( [position[0], position[1], position[2] + sizes[2]/2], [0,0, 1], material)
        backPlane = Plane ( [position[0], position[1], position[2] - sizes[2]/2], [0,0,-1], material)
        
        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)
        
        #Bounds

        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]
        
        epsilon = 0.001 # like bias
        
        for i in  range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i]/2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i]/2)
    
    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")
        for plane in self.planes:
            
            planeIntercept = plane.ray_intersect(orig, dir)
            
            if planeIntercept is not None:
                planePoint = planeIntercept.point
                
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            
                            if planeIntercept.distance < t:
                                
                                t = planeIntercept.distance
                                intercept = planeIntercept
        if intercept ==  None:
            return None
        
        return Intercept(
            point=intercept.point,
            normal=intercept.normal,
            distance=t,
            texCoords= None,
            rayDirection=dir,
            obj = self
        )