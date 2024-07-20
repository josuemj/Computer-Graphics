from MathLib import *

def vertexShader(vertex, **kwargs):
    
    modelMatrix = kwargs["modelMatrix"]

    if len(vertex) + 1 == len(modelMatrix):
        vt = vertex + [1]
    else:
        vt = vertex
    
    vt = vector_matrix_multiply(vt, modelMatrix)
    
    if vt[-1] != 0 and len(vt) > 3:
        vt = [vt[i] / vt[-1] for i in range(len(vt) - 1)]
    
    return vt