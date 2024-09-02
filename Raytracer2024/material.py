class Material(object):
    def __init__(self, difuse):
        self.difuse = difuse
        
    def GetSurfaceColor(self, intercept, renderer):
        #phong reflection model
        #LightColors = LightColor + Specular
        #FinalColor = DiffuseColor * LightColor
        
        lightColor = [0, 0, 0]
        finalColor = self.difuse
        for light in renderer.lights:
            currentLightColor = light.GetLightColor(intercept)
            lightColor = [(lightColor[i] + currentLightColor[i]) for i in range(3)]
        finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        return finalColor
    