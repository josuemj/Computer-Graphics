#gl stands for graphics libraru
import struct


def char(c):
    #1 byte
    return struct.pack("=c",c.encode("ascii"))

def word(w):
    #2 bytes
    return struct.pack("=h", w)

def dword(d):
    #4 bytes
    return struct.pack("=l", d)

class Render(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glclearColor(0,0,0)
        self.glClear()
    
    def glColor(self, r, g, b): #r, g, b on values from 0 to 1
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currentColor = [r,g,b]
    
    def glPoint(self, x, y, color = None):
        #pygame renders from top top left corner
        #but  BITMP starts from bottom left corner
        #So we have to switch the 'y' value
        if (0<=x<self.width) and (0<= y<self.height):
            #pygame receices color into a range from 0 to 255
            color = [int(i*255) for i in (color or self.currentColor)]
            self.screen.set_at((x, self.height-1-y), color)

    def glclearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r,g,b]
    
    def glClear(self):
        color = [int(i*255) for i in self.clearColor]
        self.screen.fill(color) #Screen color function
        self.frameBuffer = [[self.clearColor for y  in range(self.height) for x in range(self.width)]]
    
    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            #wb en  binario

            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(14 + 40))    

            #Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(1)
            file.write(word(24)) #Bits per pixe
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2],color[1],color[0]])
                    file.write(color)
