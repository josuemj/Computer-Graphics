from MathLib import *
from math import cos, pi, sin

class Light(object):
    def __init__(self, color = [1, 1, 1], intensity = 1.0, lighType = "None"):
        self.color = color
        self.intensity = intensity
        self.lighType = lighType
        
    def GetLightColor(self, intercept = None):
        return [(i * self.intensity) for i in self.color] 

    def GetSpecularColor(self, intercept, viewPos):
        return [0, 0, 0]
        
class AmbientLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0):
        super().__init__(color, intensity, "Ambient")
        
class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1.0, direction=[0, -1, 0]):
        super().__init__(color, intensity, "Directional")
        self.direction = normalize(direction)

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()
        if intercept:
            dir_inv = scalar_multiply(self.direction, -1)
            intensity = dotP(intercept.normal, dir_inv)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [i * intensity for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color
        if intercept:
            dir_inv = scalar_multiply(self.direction, -1)
            reflect = reflectVector(intercept.normal, dir_inv)
            viewDir = normalize(substraction(viewPos, intercept.point))
            # Clamp the dot product before raising to the power
            spec_angle = max(0, dotP(viewDir, reflect))
            specularity = spec_angle ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks * self.intensity
            specColor = [i * specularity for i in specColor]
        return specColor

class PointLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0]):
        super().__init__(color, intensity)
        self.position = position
        self.lighType = "Point"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()
        if intercept:
            dir_vec = substraction(self.position, intercept.point)
            R = norm(dir_vec)
            dir_vec = normalize(dir_vec)
            intensity = dotP(intercept.normal, dir_vec)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks) * self.intensity
            if R != 0:
                intensity /= R ** 2
            lightColor = [i * intensity for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color
        if intercept:
            dir_vec = substraction(self.position, intercept.point)
            R = norm(dir_vec)
            dir_vec = normalize(dir_vec)
            reflect = reflectVector(intercept.normal, dir_vec)
            viewDir = normalize(substraction(viewPos, intercept.point))
            # Clamp the dot product before raising to the power
            spec_angle = max(0, dotP(viewDir, reflect))
            specularity = spec_angle ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks * self.intensity
            if R != 0:
                specularity /= R ** 2
            specColor = [i * specularity for i in specColor]
        return specColor
class SpotLight(PointLight):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0], direction=[0, -1, 0], innerAngle=50, outerAngle=60):
        super().__init__(color, intensity, position)
        self.direction = normalize(direction)
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lighType = "Spot"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)
        if intercept:
            attenuation = self.SpotlightAttenuation(intercept)
            lightColor = [i * attenuation for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)
        if intercept:
            attenuation = self.SpotlightAttenuation(intercept)
            specularColor = [i * attenuation for i in specularColor]
        return specularColor

    def SpotlightAttenuation(self, intercept=None):
        if intercept is None:
            return 0
        wi = normalize(substraction(self.position, intercept.point))
        innerAngleRads = self.innerAngle * pi / 180
        outerAngleRads = self.outerAngle * pi / 180
        cosTheta = dotP(self.direction, wi)
        attenuation = (-cosTheta - cos(outerAngleRads)) / (cos(innerAngleRads) - cos(outerAngleRads))
        attenuation = min(1, max(0, attenuation))
        return attenuation