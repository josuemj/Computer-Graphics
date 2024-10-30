vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform  float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}

'''

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex, outTexCoords);   
}
'''

enhanced  = '''
#version 450 core

in vec2 outTexCoords;
in vec3 FragPos;
in vec3 Normal;

out vec4 fragColor;

uniform sampler2D tex;

uniform vec3 lightPos;    
uniform vec3 viewPos;     
uniform vec3 lightColor;  
uniform vec3 objectColor; 

void main()
{
    // Ambient lighting
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse lighting
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Specular lighting
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    // Phong specular model
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;

    // Combine all lighting components
    vec3 lighting = (ambient + diffuse + specular);

    // Texture color
    vec4 texColor = texture(tex, outTexCoords);

    // Final color with lighting applied to the texture
    fragColor = vec4(lighting, 1.0) * texColor;
}

'''

fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform  float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position + normals * sin(time) / 10, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}

'''

water_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform  float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position + vec3(0,1,0) * sin(time * position.x) /10, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}

'''

#shaders
color_inversion_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    vec4 color = texture(tex, outTexCoords);
    fragColor = vec4(1.0 - color.rgb, color.a);
}
'''

grayscale_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    vec4 color = texture(tex, outTexCoords);
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    fragColor = vec4(vec3(gray), color.a);
}
'''

edge_detection_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    float intensity = abs(dot(normalize(outNormals), vec3(0.0, 0.0, 1.0)));
    if (intensity < 0.5)
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    else
        fragColor = texture(tex, outTexCoords);
}
'''

# Shader 6: Toon Shader
toon_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    vec3 normal = normalize(outNormals);
    float intensity = dot(normal, vec3(0.0, 0.0, 1.0));
    float levels = 3.0;
    intensity = floor(intensity * levels) / levels;
    vec4 color = texture(tex, outTexCoords);
    fragColor = vec4(color.rgb * intensity, color.a);
}
'''


# shaders.py

# ... existing shaders ...

# Rainbow Shader (Fragment Shader)
rainbow_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform float time;

out vec4 fragColor;

void main()
{
    float r = sin(6.28318 * (outTexCoords.x + time * 0.1)) * 0.5 + 0.5;
    float g = sin(6.28318 * (outTexCoords.y + time * 0.1)) * 0.5 + 0.5;
    float b = sin(6.28318 * (outTexCoords.x + outTexCoords.y + time * 0.1)) * 0.5 + 0.5;

    fragColor = vec4(r, g, b, 1.0);
}
'''

# Chess Pattern Shader (Vertex Shader)
bounce_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

float easeOutBounce(float x) {
    float n1 = 7.5625;
    float d1 = 2.75;
    if (x < 1.0 / d1) {
        return n1 * x * x;
    } else if (x < 2.0 / d1) {
        x = x - 1.5 / d1;
        return n1 * x * x + 0.75;
    } else if (x < 2.5 / d1) {
        x = x - 2.25 / d1;
        return n1 * x * x + 0.9375;
    } else {
        x = x - 2.625 / d1;
        return n1 * x * x + 0.984375;
    }
}

void main()
{
    float t = mod(time, 2.0);
    if (t > 1.0) {
        t = 2.0 - t;
    }
    float bounce = easeOutBounce(t);
    float height = bounce * 0.5;
    vec3 newPosition = position + vec3(0, height, 0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

# Orange Fragment Shader
orange_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    vec3 normal = normalize(outNormals);
    vec3 lightDir = normalize(vec3(0.0, 0.0, 1.0));
    float intensity = max(dot(normal, lightDir), 0.0);
    vec3 baseColor = vec3(1.0, 0.5, 0.0);
    vec3 color = baseColor * intensity;
    fragColor = vec4(color, 1.0);
}
'''

# Pulse Vertex Shader
pulse_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Pulsing scaling effect
    float scaleValue = 1.0 + sin(time * 4.0) * 0.2; // Scales between 0.8 and 1.2
    mat4 scale = mat4(
        scaleValue, 0.0,       0.0,       0.0,
        0.0,        scaleValue, 0.0,       0.0,
        0.0,        0.0,       scaleValue, 0.0,
        0.0,        0.0,       0.0,        1.0
    );

    vec4 transformedPosition = scale * vec4(position, 1.0);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * transformedPosition;

    outTexCoords = texCoords;
    outNormals = normals;
}
'''

# Pulse Fragment Shader
pulse_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform float time;

out vec4 fragColor;

void main()
{
    float r = sin(time * 2.0) * 0.5 + 0.5;
    float g = sin(time * 3.0 + 2.0) * 0.5 + 0.5;
    float b = sin(time * 4.0 + 4.0) * 0.5 + 0.5;

    fragColor = vec4(r, g, b, 1.0);
}
'''


# Bounce Vertex Shader
bounce_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

float easeOutBounce(float x) {
    float n1 = 7.5625;
    float d1 = 2.75;
    if (x < 1.0 / d1) {
        return n1 * x * x;
    } else if (x < 2.0 / d1) {
        x = x - 1.5 / d1;
        return n1 * x * x + 0.75;
    } else if (x < 2.5 / d1) {
        x = x - 2.25 / d1;
        return n1 * x * x + 0.9375;
    } else {
        x = x - 2.625 / d1;
        return n1 * x * x + 0.984375;
    }
}

void main()
{
    float t = mod(time, 2.0);
    if (t > 1.0) {
        t = 2.0 - t;
    }
    float bounce = easeOutBounce(t);
    float height = bounce * 0.5;
    vec3 newPosition = position + vec3(0, height, 0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

# Orange Fragment Shader
orange_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    vec3 normal = normalize(outNormals);
    vec3 lightDir = normalize(vec3(0.0, 0.0, 1.0));
    float intensity = max(dot(normal, lightDir), 0.0);
    vec3 baseColor = vec3(1.0, 0.5, 0.0);
    vec3 color = baseColor * intensity;
    fragColor = vec4(color, 1.0);
}
'''


# Rainbow Vertex Shader
rainbow_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Rotate around Y-axis
    float angle = sin(time) * 0.5; // Oscillates between -0.5 and 0.5 radians

    mat4 rotation = mat4(
        cos(angle), 0.0, sin(angle), 0.0,
        0.0,        1.0, 0.0,        0.0,
       -sin(angle), 0.0, cos(angle), 0.0,
        0.0,        0.0, 0.0,        1.0
    );

    vec4 transformedPosition = rotation * vec4(position, 1.0);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * transformedPosition;

    outTexCoords = texCoords;
    outNormals = normals;
}
'''

# Rainbow Fragment Shader
rainbow_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform float time;

out vec4 fragColor;

void main()
{
    float r = sin(6.28318 * (outTexCoords.x + time * 0.1)) * 0.5 + 0.5;
    float g = sin(6.28318 * (outTexCoords.y + time * 0.1)) * 0.5 + 0.5;
    float b = sin(6.28318 * (outTexCoords.x + outTexCoords.y + time * 0.1)) * 0.5 + 0.5;

    fragColor = vec4(r, g, b, 1.0);
}
'''


# Toon Vertex Shader
toon_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Breathing effect scaling
    float scaleValue = 1.0 + sin(time * 2.0) * 0.1; // Scales between 0.9 and 1.1
    mat4 scale = mat4(
        scaleValue, 0.0,       0.0,       0.0,
        0.0,        scaleValue, 0.0,       0.0,
        0.0,        0.0,       scaleValue, 0.0,
        0.0,        0.0,       0.0,        1.0
    );

    vec4 transformedPosition = scale * vec4(position, 1.0);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * transformedPosition;

    outTexCoords = texCoords;
    outNormals = normals;
}
'''

# Toon Fragment Shader
toon_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    vec3 normal = normalize(outNormals);
    float intensity = dot(normal, vec3(0.0, 0.0, 1.0));
    float levels = 3.0;
    intensity = floor(intensity * levels) / levels;
    vec4 color = texture(tex, outTexCoords);
    fragColor = vec4(color.rgb * intensity, color.a);
}
'''


# Edge Detection Vertex Shader
edge_detection_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Rotation angle over time
    float angle = time;

    // Rotation matrix around the Y-axis
    mat4 rotation = mat4(
        cos(angle), 0.0, sin(angle), 0.0,
        0.0,        1.0, 0.0,        0.0,
       -sin(angle), 0.0, cos(angle), 0.0,
        0.0,        0.0, 0.0,        1.0
    );

    // Scaling over time
    float scaleValue = 1.0 + sin(time) * 0.5; // Scales between 0.5 and 1.5
    mat4 scale = mat4(
        scaleValue, 0.0,       0.0,       0.0,
        0.0,        scaleValue, 0.0,       0.0,
        0.0,        0.0,       scaleValue, 0.0,
        0.0,        0.0,       0.0,        1.0
    );

    vec4 rotatedPosition = rotation * vec4(position, 1.0);
    vec4 transformedPosition = scale * rotatedPosition;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * transformedPosition;

    outTexCoords = texCoords;
    outNormals = normals; // Use normals as is
}
'''

# Edge Detection Fragment Shader
edge_detection_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    float intensity = abs(dot(normalize(outNormals), vec3(0.0, 0.0, 1.0)));
    if (intensity < 0.5)
        fragColor = vec4(0.0, 0.0, 0.0, 1.0); // Edge color
    else
        fragColor = texture(tex, outTexCoords);
}
'''


# Grayscale Vertex Shader
grayscale_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // Apply a water-like movement
    float wave = sin(position.x * 5.0 + time * 2.0) * 0.1;
    vec3 newPosition = position + vec3(0.0, wave, 0.0);

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPosition, 1.0);

    outTexCoords = texCoords;
    outNormals = normals;
}
'''

grayscale_fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    vec4 color = texture(tex, outTexCoords);
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    fragColor = vec4(vec3(gray), color.a);
}
'''


