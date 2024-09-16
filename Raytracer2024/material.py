class Material(object):
    def __init__(self, difuse, spec = 1.0, Ks = 0.0):
        self.difuse = difuse
        self.spec = spec
        self.Ks = Ks
        
    def GetSurfaceColor(self, intercept, renderer):
        #phong reflection model
        #LightColors = LightColor + Specular
        #FinalColor = DiffuseColor * LightColor
        
        lightColor = [0, 0, 0]
        finalColor = self.difuse
        
        for light in renderer.lights:
            
            currentLightColor = light.GetLightColor(intercept)
            currentSpecularColor = light.GetSpecularColor(intercept, renderer.camera.translate)
            lightColor = [(lightColor[i] + currentLightColor[i] + currentSpecularColor[i]) for i in range(3)]
            
        finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        return finalColor
    