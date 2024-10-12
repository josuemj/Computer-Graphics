vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vColor;

out vec3 outColor;

void main()
{
    gl_Position = vec4(position, 1.0);
    outColor = vColor;
}

'''

fragment_shader = '''
#version 450 core

in vec3 outColor;
out vec4 fragColor;

void main()
{
    fragColor = vec4(outColor, 1.0);   
}
'''