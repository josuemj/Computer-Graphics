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
        
from math import pi, cos, sin

import numpy as np


class Pyramid(Shape):
    def __init__(self, base_center, base_size, height, material, pitch=0, yaw=0, roll=0):
        super().__init__(base_center, material)
        self.base_size = base_size
        self.height = height
        self.pitch = pitch  # Rotation around the X-axis
        self.yaw = yaw      # Rotation around the Y-axis
        self.roll = roll    # Rotation around the Z-axis
        self.type = "Pyramid"

        half_size = base_size / 2.0

        # Define the base vertices (square base)
        self.v0 = np.array([base_center[0] - half_size, base_center[1], base_center[2] - half_size])  # bottom left
        self.v1 = np.array([base_center[0] + half_size, base_center[1], base_center[2] - half_size])  # bottom right
        self.v2 = np.array([base_center[0] + half_size, base_center[1], base_center[2] + half_size])  # top right
        self.v3 = np.array([base_center[0] - half_size, base_center[1], base_center[2] + half_size])  # top left

        # Peak of the pyramid
        self.peak = np.array([base_center[0], base_center[1] + height, base_center[2]])

        # Apply rotation to the vertices
        self.apply_rotation()

        # Create triangular faces for the pyramid
        self.faces = [
            Triangle(self.v0, self.v1, self.peak, material),  # Front face
            Triangle(self.v1, self.v2, self.peak, material),  # Right face
            Triangle(self.v2, self.v3, self.peak, material),  # Back face
            Triangle(self.v3, self.v0, self.peak, material)   # Left face
        ]

    def apply_rotation(self):
        """Applies rotation to the pyramid vertices."""
        # Convert degrees to radians
        pitch_rad = self.pitch * (pi / 180)
        yaw_rad = self.yaw * (pi / 180)
        roll_rad = self.roll * (pi / 180)

        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, cos(pitch_rad), -sin(pitch_rad)],
            [0, sin(pitch_rad), cos(pitch_rad)]
        ])
        Ry = np.array([
            [cos(yaw_rad), 0, sin(yaw_rad)],
            [0, 1, 0],
            [-sin(yaw_rad), 0, cos(yaw_rad)]
        ])
        Rz = np.array([
            [cos(roll_rad), -sin(roll_rad), 0],
            [sin(roll_rad), cos(roll_rad), 0],
            [0, 0, 1]
        ])

        # Combined rotation matrix
        # The order of multiplication matters: R = Rz * Ry * Rx
        R = Rz @ Ry @ Rx

        # Apply rotation to each vertex
        for vertex in [self.v0, self.v1, self.v2, self.v3, self.peak]:
            # Translate vertex to origin
            translated_vertex = vertex - self.position
            # Apply rotation
            rotated_vertex = R @ translated_vertex
            # Translate back
            vertex[:] = rotated_vertex + self.position

    def ray_intersect(self, orig, dir):
        """Tests ray intersections with the pyramid's triangular faces."""
        closest_intercept = None
        min_distance = float('inf')

        for face in self.faces:
            intercept = face.ray_intersect(orig, dir)
            if intercept and intercept.distance < min_distance:
                closest_intercept = intercept
                min_distance = intercept.distance

        return closest_intercept

import numpy as np
from math import pi, sin, cos, sqrt
from numpy import linalg as LA

class Torus(Shape):
    def __init__(self, position, major_radius, minor_radius, material, pitch=0, yaw=0, roll=0):
        super().__init__(position, material)
        self.major_radius = major_radius  # Distance from center to the center of the tube
        self.minor_radius = minor_radius  # Radius of the tube
        self.type = "Torus"
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

        # Precompute the rotation matrix
        self.rotation_matrix = self.compute_rotation_matrix()

        # Compute the inverse rotation matrix
        self.inverse_rotation_matrix = LA.inv(self.rotation_matrix)

    def compute_rotation_matrix(self):
        """Computes the combined rotation matrix from pitch, yaw, and roll."""
        # Convert degrees to radians
        pitch_rad = self.pitch * (pi / 180)
        yaw_rad = self.yaw * (pi / 180)
        roll_rad = self.roll * (pi / 180)

        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, cos(pitch_rad), -sin(pitch_rad)],
            [0, sin(pitch_rad), cos(pitch_rad)]
        ])
        Ry = np.array([
            [cos(yaw_rad), 0, sin(yaw_rad)],
            [0, 1, 0],
            [-sin(yaw_rad), 0, cos(yaw_rad)]
        ])
        Rz = np.array([
            [cos(roll_rad), -sin(roll_rad), 0],
            [sin(roll_rad), cos(roll_rad), 0],
            [0, 0, 1]
        ])

        # Combined rotation matrix: R = Rz * Ry * Rx
        R = Rz @ Ry @ Rx
        return R

    def ray_intersect(self, orig, dir):
        """
        Computes the intersection of a ray with the torus.
        The torus is defined in object space, so we need to transform
        the ray into the torus's local coordinate system.
        """
        # Transform the ray into the torus's local space
        orig_local = np.dot(self.inverse_rotation_matrix, np.subtract(orig, self.position))
        dir_local = np.dot(self.inverse_rotation_matrix, dir)

        # Ray-Torus intersection equation coefficients
        # Based on the standard torus equation:
        # (x^2 + y^2 + z^2 + R^2 - r^2)^2 - 4*R^2*(x^2 + y^2) = 0

        G = np.dot(dir_local, dir_local)
        H = 2 * np.dot(orig_local, dir_local)
        I = np.dot(orig_local, orig_local) + self.major_radius**2 - self.minor_radius**2

        J = orig_local[0]**2 + orig_local[1]**2
        K = dir_local[0]**2 + dir_local[1]**2
        L = 2 * (orig_local[0]*dir_local[0] + orig_local[1]*dir_local[1])

        # Quartic equation coefficients: a*t^4 + b*t^3 + c*t^2 + d*t + e = 0
        a = G**2
        b = 2*G*H
        c = H**2 + 2*G*I - 4*self.major_radius**2*K
        d = 2*H*I - 4*self.major_radius**2*L
        e = I**2 - 4*self.major_radius**2*J

        # Solve the quartic equation
        coeffs = [a, b, c, d, e]
        roots = np.roots(coeffs)

        # Filter real roots and positive t values
        real_roots = [root.real for root in roots if np.isreal(root) and root.real > 0]
        if not real_roots:
            return None

        t = min(real_roots)

        # Compute the intersection point in local space
        P_local = orig_local + t * dir_local

        # Compute the normal at the intersection point in local space
        param = self.major_radius
        x, y, z = P_local
        sum_squared = x**2 + y**2 + z**2
        nx = 4 * x * (sum_squared - (param**2 + self.minor_radius**2))
        ny = 4 * y * (sum_squared - (param**2 + self.minor_radius**2))
        nz = 4 * z * (sum_squared - (param**2 + self.minor_radius**2) + 2 * param**2)

        normal_local = np.array([nx, ny, nz])
        normal_local = normal_local / LA.norm(normal_local)

        # Transform the intersection point and normal back to world space
        P_world = np.dot(self.rotation_matrix, P_local) + self.position
        normal_world = np.dot(self.rotation_matrix, normal_local)
        normal_world = normal_world / LA.norm(normal_world)

        # Compute texture coordinates (u, v)
        phi = np.arctan2(P_local[2], P_local[0])
        theta = np.arcsin(P_local[1] / self.minor_radius)
        u = (phi + pi) / (2 * pi)
        v = (theta + pi/2) / pi

        return Intercept(
            point=P_world,
            normal=normal_world,
            distance=t,
            texCoords=[u % 1.0, v % 1.0],
            rayDirection=dir,
            obj=self
        )
