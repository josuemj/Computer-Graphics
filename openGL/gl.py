import glm

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        glClearColor(0.2, 0.2, 0.2,1) # set backoground color
        
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        
        self.scene = []
    
    def Render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #clear frame buffer color and depth information
        
        for obj in self.scene:
            obj.Render()