class Material(object):
    def __init__(self, difuse):
        self.difuse = difuse
        
    def GetSurfaceColor(self):
        return self.difuse