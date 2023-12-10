from ursina import Shader


camera_grayscale_shader = Shader(
fragment='''
#version 430

uniform sampler2D tex;
in vec2 uv;
out vec4 color;

void main() {
    color = texture(tex, uv).rgba;
    float water_level = 0;

    if (color == vec4(1,0,0,1)) {
        vec2 new_uv = vec2(uv.x, -uv.y + -.365);
        color = texture(tex, new_uv).rgba * 0.75;
    }
    // color = vec4(1,1,0,1);
    // if (uv.y < .25) {
    //     color = vec4(0,0.,1.,1.);
    // }
    // color = vec4(rgb, 1.0);
}

''')



if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    # e = Entity(model='sphere', color=color.orange)
    # e = Entity(model='cube', y=-1)
    camera.shader = camera_grayscale_shader
    # camera.clip_plane_near = 1
    EditorCamera()

    # random.seed(2)
    # for i in range(20):
    #     e = Entity(model='cube', position=Vec3(random.random(),random.random(),random.random())*2, rotation=Vec3(random.random(),random.random(),random.random())*360)
    #
    plane = Entity(model='quad', scale=(20, 3), y=-3, color=color.red)
    Sprite('shore', z=2)
    def update():
        camera.x += (held_keys['d'] - held_keys['a']) * time.dt * 2
    app.run()
