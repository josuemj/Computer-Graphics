from intercept import Intercept
from math import tan, pi, atan2, acos
from MathLib import *

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
        L = substraction(self.position, orig)
        tca = dotP(L,  dir)
        
        L_norm_sq = sum([comp ** 2 for comp in L])  # ||L||^2
        d_sq = L_norm_sq - tca ** 2
        if d_sq < 0:
            return None  # No intersección
        
        d = sqrt(d_sq)
        
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
        scaledDir = [comp * t0 for comp in dir]  # direction * t0
        intersectPoint = add(orig, scaledDir)  # origin + (direction * t0)

        # normalVec = (PuntoIntersección - self.centro).normalize()
        pointDiff = substraction(intersectPoint, self.position)
        normal = normalize_vector(pointDiff)
        
        u = (atan2(normal[2], normal[0]) / (2 * pi) + 0.5)
        v = acos(-normal[1]) / pi
        
        return Intercept(point = intersectPoint, 
                         normal = normal,
                         distance = t0,
                         rayDirection=dir,
                         obj = self,
                         texCoords= [u, v]
                         )        