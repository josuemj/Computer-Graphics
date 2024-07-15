#gl stands for graphics libraru
import struct

def char(c):
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    return struct.pack("=h", w)

def dword(d):
    return struct.pack("=l", d)
class Render(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glClearColor(0, 0, 0)
        self.glClear()
    
    def glColor(self, r, g, b): #r, g, b on values from 0 to 1
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currentColor = [r,g,b]
    
    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r,g,b]
    
    def glClear(self):
        color = [int(i*255) for i in self.clearColor]
        self.screen.fill(color)

        #frame buffer
        self.frameBuffer = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

    def glPoint(self, x, y, color = None):
        #pygame renders from top top left corner
        #but  BITMP starts from bottom left corner
        #So we have to switch the 'y' value
        if (0<=x<self.width) and (0<= y<self.height):
            #pygame receices color into a range from 0 to 255
            color = [int(i*255) for i in (color or self.currentColor)]
            self.screen.set_at((x, self.height-1-y), color)

            self.frameBuffer[x][y] = color
    
    def glLine(self, v0, v1, color = None):
        #y = mx + b
        
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        #from here on we got the problem that when slope is
        #too greater than 1, the line jumps pixels
        #So we will implement a new algorithm 
        # m = (y1 - y0) / (x1 - x0)
        # b = y0 - m*x0

        # for x in range(x0, x1 + 1):
        #     y = m * x + b
        #     self.glPoint(round(x), round(y))


        """
        Bresenham line's algorithm
        """ 
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx #To sloped
        
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.75
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currentColor)
            else:
                self.glPoint(x, y, color or self.currentColor)
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1
    
    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))
            
            #Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
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
                    color = bytes([color[2], color[1], color[0]]) # on bgr instead of rgb
                    file.write(color)
    
    def glFillPolygon(self, points):
        minY = min(points, key=lambda p: p[1])[1]
        maxY = max(points, key=lambda p: p[1])[1]
        
        for y in range(minY, maxY + 1):
            nodes = []
            j = len(points) - 1
            for i in range(len(points)):
                if points[i][1] < y and points[j][1] >= y or points[j][1] < y and points[i][1] >= y:
                    nodes.append(int(points[i][0] + (y - points[i][1]) / (points[j][1] - points[i][1]) * (points[j][0] - points[i][0])))
                j = i
            nodes.sort()
            
            for n in range(0, len(nodes), 2):
                if n + 1 < len(nodes):
                    for x in range(nodes[n], nodes[n + 1] + 1):
                        self.glPoint(x, y)

