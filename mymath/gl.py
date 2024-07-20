#gl stands for graphics libraru

class Render(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
    
    def glColor(self, r,g,b):
        r = min(1,max(0,r))
        g = min(1,max(0,g))
        b = min(1,max(0,b))
        self.currentColor = [r,g,b]
        
    def glPoint(self, x,y,color = None):
        #Pygame empieza a renderizar desde la esquina superior izquierda
        #Hay que voltear el valor y cuando sea necesario
        if (0<=x<self.width) and (0<=y<self.height):
            #pygame recibe los colores en un rango de 0 a 255
            color = [int(i*255) for i in (color or self.currentColor)]
            self.screen.set_at((x, self.height-1-y), color)
    
    def glClearColor(self, r,g,b):
        r = min(1,max(0,r))
        g = min(1,max(0,g))
        b = min(1,max(0,b))
        self.clearColor = [r,g,b]

    def glClear(self):
        color = [int(i*255) for i in (color or self.clearColor)]|   
