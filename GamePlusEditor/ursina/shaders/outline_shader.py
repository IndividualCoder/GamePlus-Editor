from GamePlusEditor.ursina import *; outline_shader = Shader(language=Shader.GLSL, vertex = '''
#version 150
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 texcoords;
uniform vec2 texture_scale;
uniform vec2 texture_offset;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoords = (p3d_MultiTexCoord0 * texture_scale) + texture_offset;
}
''',
fragment='''
#version 150

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 texcoords;
out vec4 fragColor;

void main() {
    vec4 color = texture(p3d_Texture0, texcoords) * p3d_ColorScale;
    fragColor = color.rgba;
}
''',
default_input={
    'texture_scale' : (1,1),
    'texture_offset' : (0,0),
}
)



if __name__ == '__main__':
    from GamePlusEditor.ursina import *

    app = Ursina(vsync=1)

    Entity(model='cube', shader=outline_shader)
    EditorCamera()

    app.run()
