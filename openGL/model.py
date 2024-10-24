from obj import Obj
from buffer import Buffer
from pygame import image
from OpenGL.GL import *


class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)
        
        self.vertices = objFile.vertices
        self.texCoords = objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces
        
        self.texture = None
    
        self.buffer = Buffer(self.BuildBuffer())
    
    def BuildBuffer(self):
        data = []
        
        for face in self.faces:
            
            faceVerts = []
            
            for i in range(len(face)):
                
                vert = []
                
                position = self.vertices[face[i][0] - 1]
                
                for value in position:
                    vert.append(value)
                    
                    
                vts = self.texCoords[face[i][1] - 1]
                
                for value in vts:
                    vert.append(value)
                
                normals = self.normals[face[i][2] - 1]
                
                for value in normals:
                    vert.append(value)
                
                faceVerts.append(vert)
                
            for value in faceVerts[0]: data.append(value)
            for value in faceVerts[1]: data.append(value)
            for value in faceVerts[2]: data.append(value)
            if len(faceVerts) == 4:
                for value in faceVerts[0]: data.append(value)
                for value in faceVerts[2]: data.append(value)
                for value in faceVerts[3]: data.append(value)
        return data

    def AddTexture(self, textureFileName):
        self.textureSurface = image.load(textureFileName) # can also be png, jpg etc
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)
        
    def Render(self):
        
        #Dara la textura
        
        if self.texture is not None: 
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            
            glTexImage2D(
                GL_TEXTURE_2D, #Texture type
                0, #Positions
                GL_RGB, #format
                self.textureSurface.get_width(), #Width
                self.textureSurface.get_height(), #Height
                0, # Border
                GL_RGB, # format
                GL_UNSIGNED_BYTE, # Type
                self.textureData #data
            )
            
            glGenerateMipmap(GL_TEXTURE_2D)
            
        self.buffer.Render()
                
    