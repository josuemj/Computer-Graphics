from MathLib import *

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
    #per each pixel
    u, v, w = kwargs["bCoords"]
    cA, cB, cC = kwargs["vertColors"]

    r = u * cA[0] + v * cB[0] + w * cC[0]
    g = u * cA[1] + v * cB[1] + w * cC[1]
    b = u * cA[2] + v * cB[2] + w * cC[2]

    return [r, g, b]
