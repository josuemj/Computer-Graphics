from intercept import Intercept
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
        L = restar_elementos(self.position, orig)
        tca = dot(L,  dir)
        
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
        scaled_dir = [comp * t0 for comp in dir]  # dir * t0
        P = suma_vectores(orig, scaled_dir)    # orig + (dir * t0)
        
        # normal = (P - self.position).normalize()
        P_minus_position = restar_elementos(P, self.position)
        normal_vector = normalize_vector(P_minus_position)
        
        return Intercept(
            point=P,
            normal=normal_vector,
            distance=t0,
            obj=self
        )