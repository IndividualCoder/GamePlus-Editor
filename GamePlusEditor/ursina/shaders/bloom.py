from GamePlusEditor.ursina import *
shader = Shader(fragment='''
#version 430

uniform sampler2D tex;
in vec2 uv;
uniform float blur_size;
out vec4 color;

void main() {
    float pad = .2;
    vec3 offset = vec3(1.0, 2.0, 3.0);
    color  = texture(tex, uv);
    color += texture(tex, vec2(uv.x - offset.z, uv.y));
    color += texture(tex, vec2(uv.x - offset.y, uv.y));
    color += texture(tex, vec2(uv.x - offset.x, uv.y));
    color += texture(tex, vec2(min(uv.x + offset.x, pad), uv.y));
    color += texture(tex, vec2(min(uv.x + offset.y, pad), uv.y));
    color += texture(tex, vec2(min(uv.x + offset.z, pad), uv.y));
    color /= 7;
    color.w = 1.;
}
''',
# default_input = {
#
# }
)

if __name__ == '__main__':
    app = Ursina()
    window.color = color._16

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    e = Entity(model='plane', texture='grass', scale=10, y=-1)
    camera.shader = shader
    EditorCamera()
    app.run()

#     // blend.rgb
# //
# //   This shader converts to black-and-white before calculating
# //   scene brightness.  To do this, it uses a weighted average of
# //   R,G,B.  The blend parameter controls the weighting.
# //
# // desat.x
# //
# //   Desaturation level.  If zero, the bloom's color is equal to
# //   the color of the input pixel.  If one, the bloom's color is
# //   white.
# //
# // trigger.x
# //
# //   Must be equal to mintrigger.
# //
# //   mintrigger is the minimum brightness to trigger a bloom,
# //   and maxtrigger is the brightness at which the bloom
# //   reaches maximum intensity.
# //
# // trigger.y
# //
# //   Must be equal to (1.0/(maxtrigger-mintrigger)) where
# //
# //   mintrigger is the minimum brightness to trigger a bloom,
# //   and maxtrigger is the brightness at which the bloom
# //   reaches maximum intensity.
# //
