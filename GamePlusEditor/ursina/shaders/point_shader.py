from GamePlusEditor.ursina import *; point_shader = Shader(lname='point_shader', language=Shader.GLSL, vertex = '''
#version 150
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 texcoords;

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

uniform int spherical; // 1 for spherical; 0 for cylindrical


void main() {
    texcoords = p3d_MultiTexCoord0;

    vec4 world_origin = p3d_ModelMatrix * vec4(0.0, 0.0, 0.0, 1.0);
    vec4 view_origin = p3d_ModelViewMatrix * vec4(0.0, 1.0, 1.0, 1.0);
    vec4 world_pos = p3d_ModelMatrix * p3d_Vertex;
    vec4 view_pos = world_pos - world_origin + view_origin;

    vec4 clip_pos = p3d_ProjectionMatrix * view_pos;
    gl_Position = clip_pos;
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
    'spherical' : 1,
}
)



if __name__ == '__main__':
    from GamePlusEditor.ursina import *
    from GamePlusEditor.ursina.prefabs.primitives import *
    app = Ursina(vsync=1)
    camera.clip_plane_near= 1
    window.color=color.black
    Entity(model='plane', scale=10, texture='grass')

    # e = Entity(model='quad', texture='shore', shader=point_shader, x=2)
    e = Entity(model='quad', texture='shore', billboard=True, x=2)

    e.animate('x', 0, duration=5, curve=curve.linear_boomerang, loop=True, resolution=0)
    EditorCamera()
    app.run()
