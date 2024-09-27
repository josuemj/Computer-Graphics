from math import pi, sin, cos, isclose, sqrt

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
    return [scalar * comp for comp in vector]\
        