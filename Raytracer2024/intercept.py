class Intercept(object):
    def __init__(self, point, normal, distance, rayDirection, obj, texCoords):
        self.point = point
        self.normal = normal
        self.distance = distance
        self.texCoords = texCoords
        self.rayDirection = rayDirection
        self.obj = obj
        