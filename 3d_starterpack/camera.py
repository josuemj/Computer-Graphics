from MathLib import *
import numpy as np

class Camera(object):
    
    def __init__(self):
        self.translate = [0,0,0]
        self.rotate = [0,0,0]
        
        #scale no needed

    def GetViewMatrix(self):
    
        translateMat = TranslationMatrix(self.translate[0], self.translate[1], self.translate[2])
        rotateMat = RotationMatrix(self.rotate[0], self.rotate[1], self.rotate[2])

        camMatrix = matrix_multiply(translateMat, rotateMat)

        #To do own inverse
        return np.linalg.inv(camMatrix)