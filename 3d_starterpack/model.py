from obj import Obj
from MathLib import *

class Model(object):
    #This the one that will hold all .obj information file

    def __init__(self, filename):
        objFile = Obj(filename)

        self.vertices = objFile.vertices
        self.faces = objFile.faces
        self.textCoords = objFile.textCoords

        self.translate = [0,0,0]
        self.rotate = [0,0,0]
        self.scale = [1,1,1]

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(self.translate[0], self.translate[1], self.translate[2])
        rotateMat = RotationMatrix(self.rotate[0], self.rotate[1], self.rotate[2])
        scaleMat = ScaleMatrix(self.scale[0], self.scale[1], self.scale[2])

        return matrix_multiply(matrix_multiply(translateMat, rotateMat), scaleMat)
