from MathLib import *

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    if len(vertex) + 1 == len(modelMatrix):
        vt = vertex + [1]
    else:
        vt = vertex


    vpMatrix_projectMatrix = matrix_multiply(viewportMatrix, projectionMatrix)

    vpMatrix_projectMatrix_viewMatrix = matrix_multiply(vpMatrix_projectMatrix, viewMatrix)

    vpMatrix_projectMatrix_viewMatrix_model = matrix_multiply(vpMatrix_projectMatrix_viewMatrix, modelMatrix)

    vt = vector_matrix_multiply(vt, vpMatrix_projectMatrix_viewMatrix_model)

    if len(vt) > 3:
        vt = [vt[0]/vt[3], vt[1]/vt[3], vt[2]/vt[3]]

    return vt


def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requeridavt 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4 y quinta posicion del indice del vertice
    #las obtenemos y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nB = [C[5], C[6], C[7]]

    r = 1
    g = 1
    b = 1

      #P = uA + vV + wC
    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    # Se regresa el color
    return [r,g,b]

def flatShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requeridavt 
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4 y quinta posicion del indice del vertice
    #las obtenemos y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nB = [C[5], C[6], C[7]]

    r = 1
    g = 1
    b = 1

      #P = uA + vV + wC
    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    # Se regresa el color
    return [r,g,b]

def vintageYellowShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = [0, 0, 1]

    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    nA, nB, nC = A[5:], B[5:], C[5:]

    # Interpolación de las coordenadas de textura y las normales
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]
    nP = [u * nA[0] + v * nB[0] + w * nC[0], u * nA[1] + v * nB[1] + w * nC[1], u * nA[2] + v * nB[2] + w * nC[2]]

    # Normalización de la normal interpolada
    norm_length = (nP[0]**2 + nP[1]**2 + nP[2]**2)**0.5
    nP = [nP[0]/norm_length, nP[1]/norm_length, nP[2]/norm_length]

    # Calculamos la componente difusa de la iluminación
    diffuse = max(0, nP[0] * dirLight[0] + nP[1] * dirLight[1] + nP[2] * dirLight[2])

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        # Aplicar filtro amarillo y ajustar por iluminación difusa
        r = min(1.0, (texColor[0] * 0.9 + 0.1) * diffuse)  # ligeramente rojizo
        g = texColor[1] * diffuse * 0.85  # dominante amarillo
        b = texColor[2] * diffuse * 0.2  # reducir azules
    else:
        r = 0.9 * diffuse  # suave amarillo
        g = 0.85 * diffuse  # dominante amarillo
        b = 0.2 * diffuse  # casi nulo azul

    return [r, g, b]

def checkerShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]

    scale = 15 #square sacal
    tx = (u * A[3] + v * B[3] + w * C[3]) * scale
    ty = (u * A[4] + v * B[4] + w * C[4]) * scale

    # Compute the checker pattern
    if (int(tx) % 2) == (int(ty) % 2):
        return [1, 1, 1]  # White
    else:
        return [0, 0, 0]  # Black

def blueGrayShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = [0, 0, 1]

    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    nA, nB, nC = A[5:], B[5:], C[5:]

    # Interpolación de las coordenadas de textura y las normales
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]
    nP = [u * nA[0] + v * nB[0] + w * nC[0], u * nA[1] + v * nB[1] + w * nC[1], u * nA[2] + v * nB[2] + w * nC[2]]

    # Normalización de la normal interpolada
    norm_length = (nP[0]**2 + nP[1]**2 + nP[2]**2)**0.9
    nP = [nP[0] / norm_length, nP[1] / norm_length, nP[2] / norm_length]

    # Calculamos la componente difusa de la iluminación
    diffuse = max(0, nP[0] * dirLight[0] + nP[1] * dirLight[1] + nP[2] * dirLight[2])

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r = texColor[0] * diffuse * 0.3  
        g = texColor[1] * diffuse * 0.4  
        b = min(1.0, (texColor[2] * 0.95 + 0.05) * diffuse)  # still dominant blue, but brighter
    else:
        r = 0.3 * diffuse  # increase red
        g = 0.4 * diffuse  # increase green
        b = 0.95 * diffuse  # strong blue, but lighter

    # Add a slight base light to ensure the colors aren't too dark
    r = min(1.0, r + 0.1)
    g = min(1.0, g + 0.1)
    b = min(1.0, b + 0.1)

    return [r, g, b]


def greenShadow(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]  
    textura = kwargs["texture"]  
    dirLight = kwargs["dirLight"]  

    dirLight = normalize_vector(dirLight)
 
    intensidadA = max(0, dot(A[5:8], dirLight))
    intensidadB = max(0, dot(B[5:8], dirLight))
    intensidadC = max(0, dot(C[5:8], dirLight))

    # Interpolar intensidades
    intensidad = interpolate(intensidadA, intensidadB, intensidadC, u, v, w)

    # Interpolar coordenadas de textura
    vtP = [interpolate(A[3], B[3], C[3], u, v, w),
           interpolate(A[4], B[4], C[4], u, v, w)]

    # Obtener el color de la textura
    if textura:
        texColor = textura.getColor(vtP[0], vtP[1])
        r, g, b = texColor[0], texColor[1], texColor[2]
    else:
        r, g, b = 1, 1, 1

    r *= intensidad
    g *= intensidad
    b *= intensidad

    verde_r = r * 0.4 + g * 0.6  # Reducir el rojo, mezclar con verde
    verde_g = g * 0.9 + r * 0.1  # Aumentar ligeramente el verde
    verde_b = b * 0.4 + g * 0.6  # Reducir el azul, mezclar con verde

    # Asegurarse de que los colores estén dentro del rango válido
    verde_r = min(1, max(0, verde_r))
    verde_g = min(1, max(0, verde_g))
    verde_b = min(1, max(0, verde_b))

    # Devolver el color sombreado con tema verde
    return [verde_r, verde_g, verde_b]

def metallicShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Texture coordinates interpolation
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Base metallic color (dark silver)
    r, g, b = 0.4, 0.4, 0.4

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0] * 0.5 + 0.5  # Adjusted for metallic reflection
        g *= texColor[1] * 0.5 + 0.5
        b *= texColor[2] * 0.5 + 0.5

    # Simulate metallic reflection by adding highlights
    # We simulate this by creating a "fake" specular highlight
    highlight_intensity = 0.6  # This can be adjusted to make the metal shinier
    reflection_color = 1.0  # Pure white for strong reflection
    
    # Adding fake specular highlights
    r = min(1.0, r * (1.0 - highlight_intensity) + reflection_color * highlight_intensity)
    g = min(1.0, g * (1.0 - highlight_intensity) + reflection_color * highlight_intensity)
    b = min(1.0, b * (1.0 - highlight_intensity) + reflection_color * highlight_intensity)

    # Add a slight variation to simulate surface imperfections (optional)
    noise = (u * 0.05 + v * 0.05 + w * 0.05) % 0.05
    r = max(0, r - noise)
    g = max(0, g - noise)
    b = max(0, b - noise)

    return [r, g, b]