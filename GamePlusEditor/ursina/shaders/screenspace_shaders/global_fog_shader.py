from ursina import *; global_fog_shader = Shader(language=Shader.GLSL, fragment='''
#version 430

uniform sampler2D tex;
uniform sampler2D dtex;

in vec2 uv;
out vec4 color;


void main() {
    vec4 zcol = texture(dtex, uv);
    // zcol = vec4(1.0) - zcol;
    zcol *= zcol;

    color = texture(tex, uv) - zcol*zcol;
    // color = zcol;
}

''',
geometry='')



if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = global_fog_shader

    EditorCamera()
    Entity(model='plane', scale=1000, texture='grass')
    for i in range(20):
        Entity(model='cube', z=2*i)
    camera.clip_plane_near = 1
    camera.clip_plane_far = 200

    def input(key):
        if key == 'space':
            if camera.shader:
                camera.shader = None
            else:
                camera.shader = global_fog_shader


    app.run()
