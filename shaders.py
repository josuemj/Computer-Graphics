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