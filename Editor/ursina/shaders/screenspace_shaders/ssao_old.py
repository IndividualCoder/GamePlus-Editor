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

// vec3 reconstructPosition(in vec2 uv, in float z)
// {
//     float x = uv.x * 2.0f - 1.0f;
//     float y = (1.0 - uv.y) * 2.0f - 1.0f;
//     vec4 position_s = vec4(x, y, z, 1.0f);
//     mat4x4 view_projection_matrix_inverse = inverse(p3d_ViewProjectionMatrix);
//     vec4 position_v = view_projection_matrix_inverse * position_s;
//     return position_v.xyz / position_v.w;
// }
vec3 reconstructPosition(in vec2 uv, float depth) {
    float z = depth * 2.0 - 1.0;

    vec4 clipSpacePosition = vec4(uv * 2.0 - 1.0, z, 1.0);
    vec4 viewSpacePosition = inverse(p3d_ViewProjectionMatrix) * clipSpacePosition;

    // Perspective division
    viewSpacePosition /= viewSpacePosition.w;

    vec4 worldSpacePosition = inverse(p3d_ViewProjectionMatrix) * viewSpacePosition;

    return worldSpacePosition.xyz;
}

vec3 get_normal(vec2 texcoords) {
    const vec2 offset1 = vec2(0.0, 1/499.0);
    const vec2 offset2 = vec2(1/499.0, 0.0);

    float depth = texture(dtex, texcoords).r;
    float depth1 = texture(dtex, texcoords + offset1).r;
    float depth2 = texture(dtex, texcoords + offset2).r;

    vec3 p1 = vec3(offset1, depth1 - depth);
    vec3 p2 = vec3(offset2, depth2 - depth);

    vec3 normal = cross(p1, p2);
    // normal.z = -normal.z;
    normal = vec3(normal.x, normal.y, -normal.z);

    return normalize(normal);
}

void main() {
   // Far and near distances; Used to linearize the depth value.
    float far = 500.0;
    float near = 2.0;
    float depth = (2 * near) / (far + near - (texture(dtex, uv).x) * (far - near));
   // vec3 position = cameraPosition + (normalize(frustumRay) * depth);
   // vec3 normal = texture(normalTexture, st);


    // float depth = texture(dtex, uv).r;
    vec3 position = reconstructPosition(uv, depth);
    vec3 n = get_normal(uv);
    n = normalize(n);
    // n = normalize(cross(dFdx(position), dFdy(position)));
    // n = n * vec3(1, -1, 1);
    // n = vec3(n.xyz * 0.5f + 0.5f) * .5;


    // color = texture(dtex, uv).rgba;
// Compute curvature
    vec3 dx = dFdx(n);
    vec3 dy = dFdy(n);
    vec3 xneg = n - dx;
    vec3 xpos = n + dx;
    vec3 yneg = n - dy;
    vec3 ypos = n + dy;
    float z = length(position);
    z = depth;

    float curvature = (cross(xneg, xpos).y - cross(yneg, ypos).x) * 4.0 / z;

    // Compute surface properties
    vec3 light = vec3(0.0);
    vec3 ambient = vec3(curvature + 0.5);
    vec3 diffuse = vec3(0.3);
    vec3 specular = vec3(0.0);
    float shininess = 0.0;

    // Compute final color
    float cosAngle = dot(n, light);
    color.rgb = texture(tex, uv).rgb;
    color.rgb *= ambient + diffuse * max(0.0, cosAngle) + specular * pow(max(0.0, cosAngle), shininess);
    // color.rgb = n;
    // color.rgb = vec3(depth);
    // color.rgb = vec3(depth);
}
''')



if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = curvature_shader
    camera.clip_plane_near = 2
    camera.clip_plane_far = 500
    EditorCamera()

    random.seed(2)
    for i in range(20):
        e = Entity(model='cube', position=Vec3(random.random(),random.random(),random.random())*2, rotation=Vec3(random.random(),random.random(),random.random())*360)
        # e.shader = matcap_shader
        # e.texture='blender_matcap'
        # e.model.generate_normals()
    #

    app.run()
