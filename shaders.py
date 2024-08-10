from MathLib import *
import numpy as np

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    if len(vertex) + 1 == len(modelMatrix):
        vt = vertex + [1]
    else:
        vt = vertex


    vpMatrix_projectMatrix = matrix_multiply(viewportMatrix, projectionMatrix)

    vpMatrix_projectMatrix_viewMatrix = matrix_multiply(vpMatrix_projectMatrix, viewMatrix)

    vpMatrix_projectMatrix_viewMatrix_model = matrix_multiply(vpMatrix_projectMatrix_viewMatrix, modelMatrix)

    vt = vector_matrix_multiply(vt, vpMatrix_projectMatrix_viewMatrix_model)

    if len(vt) > 3:
        vt = [vt[0]/vt[3], vt[1]/vt[3], vt[2]/vt[3]]

    return vt

def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requeridavt 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]



    #sabiendo que las coordenadas de textura estan en 4 y quinta posicion del indice del vertice
    #las obtenemos y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    r = 1
    g = 1
    b = 1

      #P = uA + vV + wC
    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

      
        
    # Se regresa el color
    return [r,g,b]

def flatShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requeridavt 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4 y quinta posicion del indice del vertice
    #las obtenemos y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    #nonales

    r = 1
    g = 1
    b = 1

      #P = uA + vV + wC
    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

      
        
    # Se regresa el color
    return [r,g,b]

def gouradShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requeridavt 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4 y quinta posicion del indice del vertice
    #las obtenemos y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    normal = [
        u * nA[0] + v * nB[0], w * nC[9], 
        u * nA[1] + v * nB[1], w * nC[1], 
        u * nA[2] + v * nB[2], w * nC[2]
              ]
    
    #nonales

    r = 1
    g = 1
    b = 1

      #P = uA + vV + wC
    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    #intensity = normal DOT -dirLight

    intensity = np.dot(normal,  -np.array(dirLight))
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity
              
    # Se regresa el color
    return [r,g,b]
