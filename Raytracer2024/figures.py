import numpy as np
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
        self.normal = np.array(normal)
        self.type = "Plane"
        
    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        
        if abs(denom) < 0.0001:
            return None
        
        num = np.dot(np.subtract(self.position, orig), self.normal)
        
        t = num / denom
        
        if t < 0:
            return None
        
        P = np.add(orig, np.array(dir) * t)

        # Compute UV coordinates for the plane
        u = (P[0] - self.position[0]) % 1
        v = (P[1] - self.position[1]) % 1

        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=[u, v],
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
        
        u, v = 0, 0

        if abs(intercept.normal[0]) > 0:  # X-axis aligned plane
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]
            
        elif abs(intercept.normal[1]) > 0:  # Y-axis aligned plane
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]
            
        elif abs(intercept.normal[2]) > 0:  # Z-axis aligned plane
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))


            
        return Intercept(
            point=intercept.point,
            normal=intercept.normal,
            distance=t,
            texCoords= [u, v],
            rayDirection=dir,
            obj = self
        )

class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(None, material)  # No tiene una posición como tal
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.type = "Triangle"

        # Precalcula la normal del triángulo usando los vértices
        edge1 = substraction(self.v1, self.v0)
        edge2 = substraction(self.v2, self.v0)
        self.normal = cross_product(edge1, edge2)
        self.normal = normalize(self.normal)  # Normalizar la normal

    def ray_intersect(self, orig, dir):
        epsilon = 1e-6
        edge1 = substraction(self.v1, self.v0)
        edge2 = substraction(self.v2, self.v0)

        # Intersección del rayo con el triángulo
        h = cross_product(dir, edge2)
        a = dotP(edge1, h)

        if -epsilon < a < epsilon:
            return None  # El rayo es paralelo al triángulo

        f = 1.0 / a
        s = substraction(orig, self.v0)
        u = f * dotP(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = cross_product(s, edge1)
        v = f * dotP(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * dotP(edge2, q)

        if t > epsilon:
            P = add(orig, scalar_multiply(dir, t))  # Punto de intersección
            return Intercept(
                point=P,
                normal=self.normal,
                distance=t,
                texCoords=[u, v],  # Podemos usar (u, v) como coordenadas de textura
                rayDirection=dir,
                obj=self
            )
        else:
            return None


class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"
        self.top_center = add(position, [0, height / 2, 0])
        self.bottom_center = substraction(position, [0, height / 2, 0])

    def ray_intersect(self, orig, dir):
        # Coeficientes para la ecuación cuadrática
        a = dir[0]**2 + dir[2]**2
        b = 2 * ((orig[0] - self.position[0]) * dir[0] + (orig[2] - self.position[2]) * dir[2])
        c = (orig[0] - self.position[0])**2 + (orig[2] - self.position[2])**2 - self.radius**2

        discriminant = b**2 - 4 * a * c
        t_values = []

        if discriminant >= 0:
            sqrt_discriminant = sqrt(discriminant)
            t0 = (-b - sqrt_discriminant) / (2 * a)
            t1 = (-b + sqrt_discriminant) / (2 * a)

            for t in [t0, t1]:
                y = orig[1] + t * dir[1]
                if self.bottom_center[1] <= y <= self.top_center[1]:
                    if t > 0:
                        t_values.append(t)

        # Comprobar intersección con las tapas
        if dir[1] != 0:
            # Tapa inferior
            t_bottom = (self.bottom_center[1] - orig[1]) / dir[1]
            if t_bottom > 0:
                x_bottom = orig[0] + t_bottom * dir[0]
                z_bottom = orig[2] + t_bottom * dir[2]
                if (x_bottom - self.position[0])**2 + (z_bottom - self.position[2])**2 <= self.radius**2:
                    t_values.append(t_bottom)
            # Tapa superior
            t_top = (self.top_center[1] - orig[1]) / dir[1]
            if t_top > 0:
                x_top = orig[0] + t_top * dir[0]
                z_top = orig[2] + t_top * dir[2]
                if (x_top - self.position[0])**2 + (z_top - self.position[2])**2 <= self.radius**2:
                    t_values.append(t_top)

        if not t_values:
            return None

        t = min(t_values)
        P = add(orig, scalar_multiply(dir, t))

        # Determinar la normal y las coordenadas de textura
        if modulus(P[1] - self.top_center[1]) < 1e-6:
            # Intersección con la tapa superior
            normal = [0, 1, 0]
            u = ((P[0] - self.position[0]) / (2 * self.radius)) + 0.5
            v = ((P[2] - self.position[2]) / (2 * self.radius)) + 0.5
        elif modulus(P[1] - self.bottom_center[1]) < 1e-6:
            # Intersección con la tapa inferior
            normal = [0, -1, 0]
            u = ((P[0] - self.position[0]) / (2 * self.radius)) + 0.5
            v = ((P[2] - self.position[2]) / (2 * self.radius)) + 0.5
        else:
            # Intersección con la superficie lateral
            normal = [P[0] - self.position[0], 0, P[2] - self.position[2]]
            normal = normalize(normal)
            u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
            v = (P[1] - self.bottom_center[1]) / self.height

        # Asegurar que u y v estén en el rango [0, 1)
        u = u % 1.0
        v = v % 1.0

        return Intercept(
            point=P,
            normal=normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )