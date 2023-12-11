from GamePlusEditor.ursina import Shader;
bloom_shader = Shader(
fragment='''
#version 430

uniform sampler2D tex;
in vec2 uv;
uniform float blur_size;
out vec4 color;
in vec2 window_size;

const int samples = 8;
const vec2 offsets[samples] = vec2[](vec2(1.0,0.0), vec2(.7,.7), vec2(1.,0.), vec2(.7,-.7), vec2(0.,-1), vec2(-.7,-1), vec2(-1.,0.), vec2(-.7,.7));

void main() {
    vec4 blurred_image = vec4(.0);
    float str = .01;
    // float aspect_ratio = window_size[0] / window_size[1];
    float aspect_ratio = 16./9.;

    for (int i=0; i<samples; i++) {
        // vec2 offset_uv = uv + vec2(0., (i/(samples-1) - 0.5) * blur_size*str);
        vec2 offset_uv = (uv + (offsets[i] * str * blur_size / vec2(aspect_ratio, 1.)));
        blurred_image += texture(tex, offset_uv) /samples/2;

        //offset_uv = uv + vec2((i/(samples-1) - 0.5) * blur_size*str / aspect_ratio, 0.);
        //blurred_image += texture(tex, offset_uv) /samples/2;
    }

    color = texture(tex, uv);
    vec4 a = mix(vec4(0.), blurred_image, 1.);
    color += a;
    // color /= 2.;
    // color += blurred_image;
}
''',
default_input=dict(
    blur_size = .5,
    window_size = (1920/1080)

))

if __name__ == '__main__':
    from GamePlusEditor.ursina import *
    app = Ursina()
    window.color = color._16

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    e = Entity(model='plane', texture='grass', scale=10, y=-1)
    camera.shader = bloom_shader


    slider = ThinSlider(max=1, dynamic=True, position=(-.25, -.45))

    def set_blur():
        print(slider.value)
        camera.set_shader_input("blur_size", slider.value)

    # def update():
    #     camera.set_shader_input('blur_size', mouse.x)


    slider.on_value_changed = set_blur
    EditorCamera()

    app.run()
