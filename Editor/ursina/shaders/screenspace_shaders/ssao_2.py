from ursina import *;

def randVec(i, n):
  """Generates a random point in a hemisphere."""

  x = random.uniform(-1, 1)
  y = random.uniform(-1, 1)
  z = random.uniform( 0.5, 1)

  l = random.uniform(0.1, 1) / math.sqrt(x * x + y * y + z * z)

  scale = (i + 1.0) / n
  l *= 0.1 + 0.9 * scale * scale

  return (x * l, y * l, z * l)


VECS = [randVec(i, 8) for i in range(8)]

ssao_shader = Shader(language=Shader.GLSL,
vertex = '''
#version 410 core
layout(location = 0) in vec3 i_vertex;
out vec2 v_uv;
void main() {
    v_uv = (i_vertex.xy + 1.0) / 2.0;
    gl_Position = vec4(i_vertex, 1.0);
}
''',

fragment='''
#version 410 core

const vec3 SAMPLES[] = vec3[](%(samples)s);
const float FOCUS = 0.15f;
const float POWER = 5.0;
// uniform mat4 u_proj;
uniform mat4 p3d_ProjectionMatrixInverse;
uniform sampler2D u_random;
uniform sampler2D ntex;
// uniform sampler2D u_vertex;
layout(location = 0) out float ao;
in vec2 v_uv;
in sampler2D d_tex;

void main() {
  // Read the position, normal and the random vector.
  vec2 scale = textureSize(ntex, 0) / textureSize(u_random, 0);
  vec4 vert = texture(u_vertex, v_uv);
  vec3 norm = texture(ntex, v_uv).rgb;
  // vec3 rvec = texture(u_random, v_uv * scale).rgb;
  // Compute the btn matrix to rotate the hemisphere.
  vec3 tang = normalize(rvec - norm * dot(rvec, norm));
  vec3 btan = cross(norm, tang);
  mat3 tbn = mat3(tang, btan, norm);
  float occlusion = 0.0;
  for (int i = 0; i < %(count)d; ++i) {
    // Compute an offset from the center point & project it.
    vec3 smpl_view = tbn * SAMPLES[i] * FOCUS + vert.xyz;
    vec4 smpl_proj = p3d_ProjectionMatrixInverse * vec4(smpl_view, 1);
    smpl_proj.xyz /= smpl_proj.w;
    smpl_proj.xy = smpl_proj.xy * 0.5f + 0.5f;
    // Sample the depth.
    float depth = -texture(u_vertex, smpl_proj.xy).w;
    // Check for edges with a steep falloff.
    float range = smoothstep(0, 1, FOCUS / abs(vert.w - depth));

    // If point occluded, add it to the accumulator.
    occlusion += depth > smpl_view.z ? 1 : 0;
  }
  ao = pow(1.0 - occlusion / %(count)d, POWER);
}
''' % {
  'samples': ','.join(['vec3(%1.4f,%1.4f,%1.4f)' % v for v in VECS]),
  'count': len(VECS)
}


,
default_input = {
    # 'random_texture' : Func(load_texture, 'noise')
    'u_random' : Func(load_texture, 'noise')
}
)


if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    e = Entity(model='plane', scale=100, y=-1)
    camera.clip_plane_far = 100
    camera.shader = ssao_shader
    EditorCamera()

    def input(key):
        if key == 'space':
            if camera.shader:
                camera.shader = None
            else:
                camera.shader = ssao_shader

    app.run()
