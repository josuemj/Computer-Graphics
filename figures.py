from intercept import Intercept
from math import pi, atan2, acos, sin, sqrt
from MathLib import *


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None

    
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

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normal
        self.type = "Plane"
        
    def ray_intersect(self, orig, dir):
        denom = dotP(dir, self.normal)
        
        if abs(denom) < 0.0001:
            return None
        
        num = dotP(substraction(self.position, orig), self.normal)
        
        t = num / denom
        
        if t < 0:
            return None
        
        P = add(orig, scalar_multiply(dir,t))

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
        self.v0 = [base_center[0] - half_size, base_center[1], base_center[2] - half_size]  # Bottom left
        self.v1 = [base_center[0] + half_size, base_center[1], base_center[2] - half_size]  # Bottom right
        self.v2 = [base_center[0] + half_size, base_center[1], base_center[2] + half_size]  # Top right
        self.v3 = [base_center[0] - half_size, base_center[1], base_center[2] + half_size]  # Top left

        # Peak of the pyramid
        self.peak = [base_center[0], base_center[1] + height, base_center[2]]

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
        # Get the rotation matrix (3x3)
        R = RotationMatrix3x3(self.pitch, self.yaw, self.roll)

        # Apply rotation to each vertex
        for vertex in [self.v0, self.v1, self.v2, self.v3, self.peak]:
            # Translate vertex to origin
            translated_vertex = substraction(vertex, self.position)
            # Apply rotation
            rotated_vertex = matrix_vector_multiply(R, translated_vertex)
            # Translate back
            vertex[:] = add(rotated_vertex, self.position)

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

from math import pi, sin, cos, sqrt, atan2, acos

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
        self.rotation_matrix = RotationMatrix3x3(self.pitch, self.yaw, self.roll)

        # Compute the inverse rotation matrix
        self.inverse_rotation_matrix = inversed_matrix(self.rotation_matrix)

    def ray_intersect(self, orig, dir):
        """
        Computes the intersection of a ray with the torus using ray marching.
        """
        # Transform the ray into the torus's local space
        orig_local = matrix_vector_multiply(self.inverse_rotation_matrix, substraction(orig, self.position))
        dir_local = matrix_vector_multiply(self.inverse_rotation_matrix, dir)
        dir_local = normalize(dir_local)

        max_distance = 1000  # Maximum distance to march
        distance_traveled = 0
        max_steps = 100  # Maximum number of steps
        epsilon = 1e-4  # Desired accuracy

        point = orig_local.copy()

        for _ in range(max_steps):
            # Evaluate the SDF at the current point
            distance = self.torus_sdf(point)
            if distance < epsilon:
                # Intersection found
                P_local = point

                # Compute normal
                normal_local = self.torus_normal(P_local)

                # Transform back to world space
                P_world = add(matrix_vector_multiply(self.rotation_matrix, P_local), self.position)
                normal_world = matrix_vector_multiply(self.rotation_matrix, normal_local)
                normal_world = normalize(normal_world)

                # Compute texture coordinates (optional)
                circle_center = [P_local[0], P_local[1], 0]
                center_norm = norm(circle_center)
                if center_norm == 0:
                    u = 0
                else:
                    u = (atan2(circle_center[1], circle_center[0]) + pi) / (2 * pi)
                circle_vector = substraction(P_local, circle_center)
                v = (atan2(circle_vector[2], norm(circle_vector[:2])) + pi) / (2 * pi)

                return Intercept(
                    point=P_world,
                    normal=normal_world,
                    distance=distance_traveled,
                    texCoords=[u % 1.0, v % 1.0],
                    rayDirection=dir,
                    obj=self
                )

            distance_traveled += distance
            if distance_traveled >= max_distance:
                break

            # Move along the ray
            point = add(orig_local, scalar_multiply(dir_local, distance_traveled))

        # No intersection
        return None

    def torus_sdf(self, p):
        """
        Signed Distance Function for a torus centered at the origin.
        """
        q = [sqrt(p[0] ** 2 + p[2] ** 2) - self.major_radius, p[1]]
        return sqrt(q[0] ** 2 + q[1] ** 2) - self.minor_radius

    def torus_normal(self, p):
        """
        Computes the normal at point p on the torus surface using numerical gradient approximation.
        """
        epsilon = 1e-5
        dx = [epsilon, 0, 0]
        dy = [0, epsilon, 0]
        dz = [0, 0, epsilon]

        sdf_p = self.torus_sdf(p)

        # Approximate gradient
        gradient = [
            (self.torus_sdf(add(p, dx)) - sdf_p) / epsilon,
            (self.torus_sdf(add(p, dy)) - sdf_p) / epsilon,
            (self.torus_sdf(add(p, dz)) - sdf_p) / epsilon
        ]
        normal = normalize(gradient)
        return normal
    
class Box(Shape):
    def __init__(self, position, sizes, material, pitch=0, yaw=0, roll=0):
        super().__init__(position, material)
        self.sizes = sizes  # [width, height, depth]
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.type = "Box"

        # Define the 8 vertices of the box
        self.vertices = self.create_vertices()
        self.apply_rotation()
        self.faces = self.create_faces()

    def create_vertices(self):
        half_sizes = [s / 2.0 for s in self.sizes]
        return [
            [self.position[0] - half_sizes[0], self.position[1] - half_sizes[1], self.position[2] - half_sizes[2]],  # Vertex 0
            [self.position[0] + half_sizes[0], self.position[1] - half_sizes[1], self.position[2] - half_sizes[2]],  # Vertex 1
            [self.position[0] + half_sizes[0], self.position[1] + half_sizes[1], self.position[2] - half_sizes[2]],  # Vertex 2
            [self.position[0] - half_sizes[0], self.position[1] + half_sizes[1], self.position[2] - half_sizes[2]],  # Vertex 3
            [self.position[0] - half_sizes[0], self.position[1] - half_sizes[1], self.position[2] + half_sizes[2]],  # Vertex 4
            [self.position[0] + half_sizes[0], self.position[1] - half_sizes[1], self.position[2] + half_sizes[2]],  # Vertex 5
            [self.position[0] + half_sizes[0], self.position[1] + half_sizes[1], self.position[2] + half_sizes[2]],  # Vertex 6
            [self.position[0] - half_sizes[0], self.position[1] + half_sizes[1], self.position[2] + half_sizes[2]]   # Vertex 7
        ]

    def apply_rotation(self):
        # Get the rotation matrix (3x3)
        R = RotationMatrix3x3(self.pitch, self.yaw, self.roll)

        # Apply rotation to each vertex
        for i in range(len(self.vertices)):
            # Translate vertex to origin
            translated_vertex = substraction(self.vertices[i], self.position)
            # Apply rotation
            rotated_vertex = matrix_vector_multiply(R, translated_vertex)
            # Translate back
            self.vertices[i] = add(rotated_vertex, self.position)

    def create_faces(self):
        """Create triangular faces from vertices."""
        faces = [
            # Front face
            (0, 1, 2), (0, 2, 3),
            # Back face
            (4, 5, 6), (4, 6, 7),
            # Left face
            (0, 3, 7), (0, 7, 4),
            # Right face
            (1, 5, 6), (1, 6, 2),
            # Top face
            (3, 2, 6), (3, 6, 7),
            # Bottom face
            (0, 1, 5), (0, 5, 4)
        ]

        triangles = []
        for face in faces:
            v0 = self.vertices[face[0]]
            v1 = self.vertices[face[1]]
            v2 = self.vertices[face[2]]
            triangles.append(Triangle(v0, v1, v2, self.material))
        return triangles

    def ray_intersect(self, orig, dir):
        closest_intercept = None
        min_distance = float('inf')

        for face in self.faces:
            intercept = face.ray_intersect(orig, dir)
            if intercept and intercept.distance < min_distance:
                closest_intercept = intercept
                min_distance = intercept.distance

        return closest_intercept
