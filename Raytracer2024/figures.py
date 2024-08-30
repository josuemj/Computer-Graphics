import numpy as np

class Shape(object):
    def __init__(self, position):
        self.position = position
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return False

    
class Sphere(Shape):
    def __init__(self, position, radius):
        super().__init__( position)
        self.radius = radius
        self.type = "Sphere"
        
    def ray_intersect(self, orig, dir):
        L = np.subtract(self.position, orig)
        tca = np.dot(L,  dir)
        d = (np.linalg.norm(L) ** 2 - tca ** 2) ** 0.5
        
        if d > self.radius:
            return False
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 < 0: 
            t0 = t1 
        if t0 < 0:
            return False
        
        # P = orig + dir * t0
        P = np.add(orig, np.multiply(dir, t0))
        return True        