from GamePlusEditor.ursina import *; fresnel_shader = Shader(language=Shader.GLSL, vertex = '''#version 150


uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 texcoords;

in vec3 p3d_Normal;
uniform mat4 p3d_ModelMatrix;
out vec3 world_normal;
out vec3 world_position;

uniform mat3 p3d_NormalMatrix;
out vec3 view_normal;



void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoords = p3d_MultiTexCoord0;

    world_position = mat3(p3d_ModelMatrix) * p3d_Vertex.xyz;
    world_normal = normalize(mat3(p3d_ModelMatrix) * p3d_Normal);
    view_normal = normalize(p3d_NormalMatrix * p3d_Normal);

    // vec3 posWorld = mul(_Object2World, v.vertex).xyz;
	// vec3 normWorld = normalize(mul(float3x3(_Object2World), v.normal));

	// vec3 I = normalize(world_position - _WorldSpaceCameraPos.xyz);
    // float power = 1.0;
	// o.R = _Bias + _Scale * pow(1.0 + dot(I, world_normal), _Power);

}
''',

fragment='''
#version 140

uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;
in vec2 texcoords;
out vec4 fragColor;

in vec3 world_normal;
in vec3 view_normal;

// uniform mat4 p3d_ViewMatrixInverse;
in vec3 world_position;
in vec3 p3d_Normal;
uniform mat4 p3d_ModelMatrix;
in vec4 p3d_Vertex;




void main() {
    vec4 color = texture(p3d_Texture0, texcoords) * p3d_ColorScale;

    // vec3 cam_dir = -p3d_ViewMatrixInverse[2].xyz;
    // viewDir = ObjSpaceViewDir(v.vertex);
    // vec3 normal
    vec3 viewDir = normalize(camera_world_position - p3d_Vertex);
    // vec3 viewDir = mat3(p3d_ModelMatrix) * p3d_Vertex.xyz;
    float fresnel = dot(normalize(p3d_Normal.xyz), normalize(-viewDir));
    // fresnel = clamp(1 - fresnel, 0.0, 1.0);
    // fresnel = 1-fresnel;
    // vec3 cam_pos = p3d_ViewMatrixInverse[3].xyz;
    // vec3 I = normalize(world_position - cam_pos.xyz);
    //
    // float fresnel = dot(world_normal, view_normal);
    // // fresnel = clamp(fresnel, 0.0, 1.0);
    // // color.rgb = vec3(fresnel);
    // R = _Bias + _Scale * pow(1.0 + dot(I, normWorld), _Power);
    //
    // vec4 fresnel_color = vec4(1,1,1,.5)
    // // color.rgb = dot(view_normal, world_normal);
    // color.rgb = vec3(fresnel * 0);
    color.rgb += fresnel * 1;
    // color.rgb += fresnel * fresnel_color.rgb * fresnel_color.a;
    // color.rgb = vec3(.5);

    fragColor = color.rgba;
}

''',
)



if __name__ == '__main__':
    from GamePlusEditor.ursina import *
    from GamePlusEditor.ursina.prefabs.primitives import *
    app = Ursina()
    window.color=color.black
    # from ursina.lights import DirectionalLight
    # DirectionalLight()



    shader = fresnel_shader

    a = AzureCube(shader=shader)
    b = BlackSphere(shader=shader, rotation_y=180, x=3)
    # b.model.generate_normals()
    # from panda3d.core import Material
    # myMaterial = Material()
    # myMaterial.setShininess(5.0) #Make this material shiny
    # myMaterial.setAmbient((0, 0, 1, 1)) #Make this material blue
    # b.set_material(myMaterial)
    # AzureSphere(shader=a.shader, y=2)
    GrayPlane(scale=10, y=-2, texture='shore', shader=shader)

    from panda3d.core import *
    # Add a sun source.
    sun = DirectionalLight("sun")
    # sun.set_color_temperature(6000)
    sun.color = color.white
    sun_path = render.attach_new_node(sun)
    sun_path.set_pos(10, 10, -10)
    sun_path.look_at(0, 0, 0)
    # sun_path.hprInterval(10.0, (sun_path.get_h(), sun_path.get_p() - 360, sun_path.get_r()), bakeInStart=True).loop()
    render.set_light(sun_path)

    # Enable shadows; we need to set a frustum for that.
    sun.get_lens().set_near_far(1, 30)
    sun.get_lens().set_film_size(20, 40)
    # sun.show_frustum()
    sun.set_shadow_caster(True, 1024, 1024)

    bmin, bmax = scene.get_tight_bounds(sun_path)
    lens = sun.get_lens()
    lens.set_film_offset((bmin.xy + bmax.xy) * 0.5)
    lens.set_film_size(bmax.xy - bmin.xy)
    lens.set_near_far(bmin.z, bmax.z)

    Sky(color=color.light_gray)
    EditorCamera()

    app.run()
