#gl stands for graphics libraru

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

    def glPoint(self, x, y, color = None):
        #pygame renders from top top left corner
        #but  BITMP starts from bottom left corner
        #So we have to switch the 'y' value
        if (0<=x<self.width) and (0<= y<self.height):
            #pygame receices color into a range from 0 to 255
            color = [int(i*255) for i in (color or self.currentColor)]
            self.screen.set_at((x, self.height-1-y), color)
    
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
            