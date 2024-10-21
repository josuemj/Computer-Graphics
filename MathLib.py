from math import pi, sin, cos, sqrt, atan2, acos

def barycentricCoords(A, B, C, P):
	
	# Se saca el �rea de los subtri�ngulos y del tri�ngulo
	# mayor usando el Shoelace Theorem, una f�rmula que permite
	# sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el �rea del tri�ngulo es 0, retornar nada para
	# prevenir divisi�n por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baric�ntricas dividiendo el 
	# �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC


	# Si cada coordenada est� entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son v�lidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None
	

def TranslationMatrix(x, y, z):
	
	return [[1, 0, 0, x],
					  [0, 1, 0, y],
					  [0, 0, 1, z],
					  [0, 0, 0, 1]]

def ScaleMatrix(x, y, z):
	
	return [[x, 0, 0, 0],
					  [0, y, 0, 0],
					  [0, 0, z, 0],
					  [0, 0, 0, 1]]

def RotationMatrix(pitch, yaw, roll):
	
	# Convertir a radianes
	pitch *= pi/180
	yaw *= pi/180
	roll *= pi/180
	
	# Creamos la matriz de rotaci�n para cada eje.
	pitchMat = [[1,0,0,0],
						  [0,cos(pitch),-sin(pitch),0],
						  [0,sin(pitch),cos(pitch),0],
						  [0,0,0,1]]
	
	yawMat = [[cos(yaw),0,sin(yaw),0],
						[0,1,0,0],
						[-sin(yaw ),0,cos(yaw),0],
						[0,0,0,1]]
	
	rollMat = [[cos(roll),-sin(roll),0,0],
						 [sin(roll),cos(roll),0,0],
						 [0,0,1,0],
						 [0,0,0,1]]
	
	return  matrix_multiply(matrix_multiply(pitchMat,yawMat), rollMat)
	

def substraction(A, B):
    if len(A) != len(B):
        raise ValueError("Must be same size")
    return [a - b for a, b in zip(A, B)]

def dotP(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))

def add(v1, v2):
    
    if len(v1) != len(v2):
        raise ValueError("Las listas deben tener la misma longitud.")
    return [a + b for a, b in zip(v1, v2)]

def reflectVector(normal, direction):
	#R = 2 * (N . L) * N - L
	dotp = dotP(normal, direction)
	norm_scale = [2 * dotp * comp for comp in normal]  # 2 * (N . L) * N
	reflect_vector = substraction(norm_scale, direction)  # 2 * (N . L) * N - L

    # Normalizar el vector reflejado
	scale = sqrt(sum([comp ** 2 for comp in reflect_vector]))
	return [comp / scale for comp in reflect_vector]

def inversed_matrix(matrix):
    
    n = len(matrix)
    
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    augmented_matrix = [row + identity_row for row, identity_row in zip(matrix, identity)]
    
    for i in range(n):
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible.")
        
        for j in range(2 * n):
            augmented_matrix[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    
    inverse_matrix = [row[n:] for row in augmented_matrix]
    
    return inverse_matrix

def normalize_vector(v):
    magnitud = (v[0]**2 + v[1]**2 + v[2]**2) ** 0.5
    return [v[0] / magnitud, v[1] / magnitud, v[2] / magnitud]

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix.")
    
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
 
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def norm(v):
    return sqrt(sum([comp ** 2 for comp in v]))

# Función para normalizar un vector
def normalize(v):
    vector_norm = norm(v)
    if vector_norm == 0:
        raise ValueError("La norma del vector es 0, no se puede normalizar.")
    return [comp / vector_norm for comp in v]

def scalar_multiply(vector, scalar):
    return [scalar * comp for comp in vector]


def cross_product(u, v):
    if len(u) != 3 or len(v) != 3:
        raise ValueError("Los vectores deben ser de 3 dimensiones.")
    return [
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0]
    ]

def modulus(x):
    return x if x >= 0 else -x


def RotationMatrix3x3(pitch, yaw, roll):
    # Convert degrees to radians
    pitch_rad = pitch * (pi / 180)
    yaw_rad = yaw * (pi / 180)
    roll_rad = roll * (pi / 180)

    Rx = [
        [1, 0, 0],
        [0, cos(pitch_rad), -sin(pitch_rad)],
        [0, sin(pitch_rad), cos(pitch_rad)]
    ]
    Ry = [
        [cos(yaw_rad), 0, sin(yaw_rad)],
        [0, 1, 0],
        [-sin(yaw_rad), 0, cos(yaw_rad)]
    ]
    Rz = [
        [cos(roll_rad), -sin(roll_rad), 0],
        [sin(roll_rad), cos(roll_rad), 0],
        [0, 0, 1]
    ]

    # Combined rotation matrix: R = Rz * Ry * Rx
    R = matrix_multiply(matrix_multiply(Rz, Ry), Rx)
    return R

def matrix_vector_multiply(matrix, vector):
    result = []
    for row in matrix:
        result.append(sum(row[i] * vector[i] for i in range(len(vector))))
    return result

def solve_quadratic(a, b, c):
    """
    Solves the quadratic equation a*t^2 + b*t + c = 0.
    Returns a list of real roots.
    """
    if a == 0:
        if b != 0:
            return [-c / b]
        else:
            return []
    else:
        discriminant = b**2 - 4 * a * c
        if discriminant > 0:
            sqrt_discriminant = sqrt(discriminant)
            t1 = (-b + sqrt_discriminant) / (2 * a)
            t2 = (-b - sqrt_discriminant) / (2 * a)
            return [t1, t2]
        elif discriminant == 0:
            t = -b / (2 * a)
            return [t]
        else:
            return []
    
def sqrt(x):
    """Computes the square root of x."""
    if x >= 0:
        return x ** 0.5
    else:
        return complex(0, (-x) ** 0.5)

def cube_root(x):
    """Computes the cube root of x."""
    if x >= 0:
        return x ** (1/3)
    else:
        return -(-x) ** (1/3)

def is_real(x):
    """Checks if a number is real (not complex)."""
    return isinstance(x, float) or (isinstance(x, complex) and x.imag == 0)


def solve_quartic(a, b, c, d, e):
    """
    Solves the quartic equation a*t^4 + b*t^3 + c*t^2 + d*t + e = 0.
    Returns a list of real roots.
    """
    # Normalize coefficients
    if a == 0:
        # It's actually a cubic equation
        return solve_cubic(b, c, d, e)
    else:
        b /= a
        c /= a
        d /= a
        e /= a

    # Depressed quartic: t^4 + p t^2 + q t + r = 0
    p = c - (3 * b**2) / 8
    q = b**3 / 8 - b * c / 2 + d
    r = -3 * b**4 / 256 + b**2 * c / 16 - b * d / 4 + e

    # Solve the resolvent cubic
    cubic_coeffs = [1, -p / 2, -r, (r * p - q**2 / 4)]
    y_solutions = solve_cubic(*cubic_coeffs)

    # Select one real solution
    y = None
    for sol in y_solutions:
        if sol.imag == 0:
            y = sol.real
            break

    if y is None:
        return []  # No real roots

    # Compute parameters
    W = sqrt(0.25 * b**2 - c + y)
    if W == 0:
        D = sqrt(3 * b**2 / 4 - 2 * c + 2 * sqrt(y**2 - 4 * e))
        E = sqrt(3 * b**2 / 4 - 2 * c - 2 * sqrt(y**2 - 4 * e))
    else:
        D = sqrt(0.75 * b**2 - W**2 - 2 * c + (0.25 * (4 * b * c - 8 * d - b**3)) / W)
        E = sqrt(0.75 * b**2 - W**2 - 2 * c - (0.25 * (4 * b * c - 8 * d - b**3)) / W)

    # Possible roots
    roots = []
    for sign_W in [1, -1]:
        for sign_D in [1, -1]:
            t = -b / 4 + sign_W * W / 2 + sign_D * D / 2
            if is_real(t):
                roots.append(t)

    return roots

def solve_cubic(a, b, c, d):
    if a == 0:
        # It's actually a quadratic equation
        return solve_quadratic(b, c, d)
    else:
        b /= a
        c /= a
        d /= a

    # Depressed cubic: t^3 + p t + q = 0
    p = c - b**2 / 3
    q = 2 * b**3 / 27 - b * c / 3 + d

    # Discriminant
    discriminant = (q / 2)**2 + (p / 3)**3

    roots = []
    if discriminant > 0:
        # One real root
        u = cube_root(-q / 2 + sqrt(discriminant))
        v = cube_root(-q / 2 - sqrt(discriminant))
        t = u + v - b / 3
        roots.append(t)
    elif discriminant == 0:
        # Triple root or one real and a double root
        u = cube_root(-q / 2)
        t1 = 2 * u - b / 3
        t2 = -u - b / 3
        roots.extend([t1, t2])
    else:
        # Three real roots
        r = sqrt(-p**3 / 27)
        phi = acos(-q / (2 * r))
        r = cube_root(r)
        t1 = 2 * r * cos(phi / 3) - b / 3
        t2 = 2 * r * cos((phi + 2 * pi) / 3) - b / 3
        t3 = 2 * r * cos((phi + 4 * pi) / 3) - b / 3
        roots.extend([t1, t2, t3])

    return roots






