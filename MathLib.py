from math import pi, sin, cos,sqrt

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
	

def reflectVector(normal, direction):
    # R = 2 * (N . L) * N - L
    dot_product = dot(normal, direction)
    scaled_normal = [2 * dot_product * n for n in normal]  # 2 * (N . L) * N
    reflect = restar_elementos(scaled_normal, direction)  # 2 * (N . L) * N - L
    
    # Normalizar el vector de reflexión
    norm = sqrt(sum([comp ** 2 for comp in reflect]))
    reflect_normalized = [comp / norm for comp in reflect]
    
    return reflect_normalized

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix.")
    
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

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

def vector_matrix_multiply(vector, matrix):
    if len(matrix[0]) != len(vector):
        raise ValueError("The number of columns in the matrix must match the size of the vector.")
    
    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]
    
    return result

def normalize_vector(v):
    magnitud = (v[0]**2 + v[1]**2 + v[2]**2) ** 0.5
    return [v[0] / magnitud, v[1] / magnitud, v[2] / magnitud]

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def interpolate(valA, valB, valC, u, v, w):
    return u * valA + v * valB + w * valC

def restar_elementos(lista1, lista2):
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud.")
    return [a - b for a, b in zip(lista1, lista2)]

def suma_vectores(lista1, lista2):
    """
    Suma elemento a elemento dos listas de igual longitud.
    """
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud.")
    return [a + b for a, b in zip(lista1, lista2)]