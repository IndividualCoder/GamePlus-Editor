from ursina import Shader


curvature_shader = Shader(
fragment='''
#version 430

uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ViewProjectionMatrix;
// uniform mat4 view_projection_matrix_inverse;

uniform sampler2D tex;
uniform sampler2D dtex;
// uniform sampler2D ntex;
in vec2 uv;
out vec4 color;

vec3 reconstructPosition(in vec2 uv, in float z)
{
    float x = uv.x * 2.0f - 1.0f;
    float y = (1.0 - uv.y) * 2.0f - 1.0f;
    vec4 position_s = vec4(x, y, z, 1.0f);
    mat4x4 view_projection_matrix_inverse = inverse(p3d_ViewProjectionMatrix);
    vec4 position_v = view_projection_matrix_inverse * position_s;
    return position_v.xyz / position_v.w;
}
// vec3 reconstructPosition(in vec2 uv, float depth) {
//     float z = depth * 2.0 - 1.0;
//
//     vec4 clipSpacePosition = vec4(uv * 2.0 - 1.0, z, 1.0);
//     vec4 viewSpacePosition = inverse(p3d_ViewProjectionMatrix) * clipSpacePosition;
//
//     // Perspective division
//     viewSpacePosition /= viewSpacePosition.w;
//
//     vec4 worldSpacePosition = inverse(p3d_ViewProjectionMatrix) * viewSpacePosition;
//
//     return worldSpacePosition.xyz;
// }

vec3 get_normal(vec2 texcoords) {
    const vec2 offset1 = vec2(0.0, 0.001);
    const vec2 offset2 = vec2(0.001, 0.0);

    float depth = texture(dtex, texcoords).r;
    float depth1 = texture(dtex, texcoords + offset1).r;
    float depth2 = texture(dtex, texcoords + offset2).r;

    vec3 p1 = vec3(offset1, depth1 - depth);
    vec3 p2 = vec3(offset2, depth2 - depth);

    vec3 normal = cross(p1, p2);
    normal.z = -normal.z;

    return normalize(normal);
}

// uniform float gSampleRad;
uniform mat4 gProj;
const int MAX_KERNEL_SIZE = 128;
uniform vec3 gKernel[MAX_KERNEL_SIZE];

void main() {
    float z = texture(dtex, uv).r;
    // depth = depth*depth;
    vec3 position = reconstructPosition(uv, z);
    vec3 n = get_normal(uv);
    // n = normalize(cross(dFdx(position), dFdy(position)));
    // n.z *= -1;
    // n.y *= -1;
    // n = n * vec3(1, -1, 1);
    // n = vec3(n.xyz * 0.5f + 0.5f) * .5;

    float AO = 0.0;
    float gSampleRad = .05;

    for (int i = 0 ; i < MAX_KERNEL_SIZE ; i++) {
        vec3 samplePos = position + gKernel[i]; // generate a random point
        vec4 offset = vec4(samplePos, 1.0); // make it a 4-vector
        offset = gProj * offset; // project on the near clipping plane
        offset.xy /= offset.w; // perform perspective divide
        offset.xy = offset.xy * 0.5 + vec2(0.5); // transform to (0,1) range

        // float sampleDepth = texture(gPositionMap, offset.xy).b;
        float sampleDepth = texture(dtex, offset.xy).b;

        if (abs(position.z - sampleDepth) < gSampleRad) {
            AO += step(sampleDepth,samplePos.z);
        }
    }

    AO = 1.0 - AO/128.0;

    color = vec4(pow(AO, 2.0));
}
''')



if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = curvature_shader
    camera.clip_plane_near = 4
    camera.clip_plane_far = 500
    # camera.set_shader_input('contrast', 1)
    EditorCamera()
    #
    # def input(key):
    #     if key == 'space':
    #         if hasattr(camera, '_shader') and camera.shader:
    #             camera.shader = None
    #         else:
    #             camera.shader = curvature_shader
    # # from ursina.shaders import matcap_shader

    random.seed(2)
    for i in range(20):
        e = Entity(model='cube', position=Vec3(random.random(),random.random(),random.random())*2, rotation=Vec3(random.random(),random.random(),random.random())*360)
        # e.shader = matcap_shader
        # e.texture='blender_matcap'
        # e.model.generate_normals()


    app.run()
