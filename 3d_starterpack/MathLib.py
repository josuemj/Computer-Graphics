from math import pi, sin, cos # sin, cos works on rads
import numpy as np
import baryCoods

def TranslationMatrix(x, y, z):
    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def ScaleMatrix(x, y, z):
    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]

def RotationMatrix(pitch, yaw, roll):
    #convert to rads
    pitch *= pi/180
    yaw *= pi/180
    roll *= pi/180

    pitchMat = [[1,0,0,0],
                      [0,cos(pitch),-sin(pitch),0],
                      [0,sin(pitch),cos(pitch),0],
                      [0,0,0,1]]

    yawMat = [[cos(yaw),0,sin(yaw),0],
                        [0,1,0,0],
                        [-sin(yaw),0,cos(yaw),0],
                        [0,0,0,1]]

    rollMat = [[cos(roll),-sin(roll),0,0],
                        [sin(roll),cos(roll),0,0],
                        [0,0,1,0],
                        [0,0,0,1]]
    
    return matrix_multiply(matrix_multiply(pitchMat,yawMat), rollMat)

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix.")
    
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def vector_matrix_multiply(vector, matrix):
    if len(matrix[0]) != len(vector):
        raise ValueError("The number of columns in the matrix must match the size of the vector.")
    
    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]
    
    return result

#TO DO own funciton
def inversed_matrix(matrix):
    
    inverse_matrix = np.linalg.inv(matrix)

    return inverse_matrix

def magnitud_vector(A):
    return []

matrix = [
    [2, 5, 7, 6],
    [1, 3, 4, 5],
    [3, 4, 5, 6],
    [5, 7, 8, 9]
]

inverse = inversed_matrix(matrix)
for row in inverse:
    print(row)

from math import isclose

def barycentricCoords(A, B, C, P):
	
	# Se saca el área de los subtriángulos y del triángulo
	# mayor usando el Shoelace Theorem, una fórmula que permite
	# sacar el área de un polígono de cualquier cantidad de vértices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el área del triángulo es 0, retornar nada para
	# prevenir división por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baricéntricas dividiendo el 
	# área de cada subtriángulo por el área del triángulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC

	# Si cada coordenada está entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son válidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
		return (u, v, w)
	else:
		return None