from MathLib import *

def vertexShader(vertex, **kwargs):
    
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]

    if len(vertex) + 1 == len(modelMatrix):
        vt = vertex + [1]
    else:
        vt = vertex
    
    #vt = matrix_multiply(viewMatrix,vector_matrix_multiply(modelMatrix, vt))
    vt1 = matrix_multiply(viewMatrix,modelMatrix)
    vt2 = matrix_multiply(vt1,vt)
    
    if vt[-1] != 0 and len(vt) > 3:
        vt = [vt[i] / vt[-1] for i in range(len(vt) - 1)]
    
    return vt2