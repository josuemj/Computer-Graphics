#Create a class that read obj file}
class Obj(object):
    def __init__(self, filename):
        #assuming file is .obj
        with open(filename, "r") as file:
            lines = file.read().splitlines() #reads each line
        self.vertices = []
        self.textCoords = []
        self.normals = []
        self.faces = []

        for line in lines:
            #If line does not count with prefix and value
            #We go the next line
            try:
                prefix, value = line.split(" ", 1)
                #print(prefix, value)
            except:
                continue

            #Depending on prefix, 
            #We will parse and save the information in the 
            #correct container

            if prefix == "v": #vertex
                vert = list(map(float, value.split(" ")))
                self.vertices.append(vert)
            
            elif prefix == "vt": #texture coords
                vts = list(map(float, value.split(" ")))
                self.textCoords.append(vts)
            
            elif prefix == "vn": #normlas
                norm = list(map(float, value.split(" ")))
                self.normals.append(norm)
            
            elif prefix == "f":
                face = []
                verts = value.split(" ")
                for vert in verts:
                    vert = list(map(int, vert.split("/")))
                    face.append(vert)
                self.faces.append(face)