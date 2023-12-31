from GamePlusEditor.ursina import *; fading_shadows_shader = Shader(language=Shader.GLSL, vertex = '''#version 150

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

in vec4 vertex;
in vec3 normal;

in vec2 p3d_MultiTexCoord0;
out vec2 texcoords;

out vec3 vpos;
out vec3 norm;


// uniform float4x4 trans_model_to_clip_of_light,
// #              uniform float4x4 mat_modelproj,
// #              uniform float4 mspos_light,
// #              uniform float4 k_ambient,
// #              uniform float4 k_scale,
// #              uniform float4 k_push,
// #
// #              out float4 l_position : POSITION,
// #              out float2 l_texcoord0 : TEXCOORD0,
// #              out float4 l_shadowcoord : TEXCOORD1,
// # 	     out float  l_smooth : TEXCOORD2,
// # 	     out float4 l_lightclip : TEXCOORD3

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  vpos = vec3(p3d_ModelViewMatrix * vertex);
  norm = normalize(p3d_NormalMatrix * normal);
  texcoords = p3d_MultiTexCoord0;
}
''',
fragment='''
in vec3 vpos;
in vec3 norm;

out vec4 p3d_FragColor;

void main() {
  p3d_FragColor = texture(p3d_Texture0, texcoords) * p3d_ColorScale;


  }
  p3d_FragColor.a = 1;
}


''',
)
if __name__ == '__main__':
    from GamePlusEditor.ursina import *
    from GamePlusEditor.ursina.prefabs.primitives import *
    app = Ursina()
    shader = fading_shadows_shader

    a = AzureCube(shader=shader, texture='shore')
    b = WhiteSphere(shader=shader, rotation_y=180, x=3, texture='brick')
    b.texture.filtering = None
    GrayPlane(scale=10, y=-2, texture='shore', shader=shader)

    Sky(color=color.light_gray)
    EditorCamera()

    def update():
        a.x += held_keys['d'] * .1
        a.x -= held_keys['a'] * .1
        a.y += held_keys['e'] * .1
        a.y -= held_keys['q'] * .1


    app.run()


# //Cg
#
# void vshader(float4 vtx_position : POSITION,
#              float2 vtx_texcoord0: TEXCOORD0,
#              float3 vtx_normal: NORMAL,
#
#              uniform float4x4 trans_model_to_clip_of_light,
#              uniform float4x4 mat_modelproj,
#              uniform float4 mspos_light,
#              uniform float4 k_ambient,
#              uniform float4 k_scale,
#              uniform float4 k_push,
#
#              out float4 l_position : POSITION,
#              out float2 l_texcoord0 : TEXCOORD0,
#              out float4 l_shadowcoord : TEXCOORD1,
# 	     out float  l_smooth : TEXCOORD2,
# 	     out float4 l_lightclip : TEXCOORD3
#              )
#
# {
# float4 position = vtx_position * k_scale;
#
# // vertex position
# l_position = mul(mat_modelproj, position);
#
# // Pass through texture coordinate for main texture.
# l_texcoord0 = vtx_texcoord0;
#
# // Calculate the surface lighting factor.
# l_smooth = saturate(dot(vtx_normal, normalize(mspos_light - position)));
#
# // Calculate light-space clip position.
# float4 pushed = position + float4(vtx_normal * k_push, 0);
# l_lightclip = mul(trans_model_to_clip_of_light, pushed);
#
# // Calculate shadow-map texture coordinates.
# l_shadowcoord = l_lightclip * float4(0.5,0.5,0.5,1.0) + l_lightclip.w * float4(0.5,0.5,0.5,0.0);
# }
#
#
# void fshader(in float2 l_texcoord0 : TEXCOORD0,
#              in float4 l_shadowcoord : TEXCOORD1,
#              in float  l_smooth : TEXCOORD2,
#              in float4 l_lightclip : TEXCOORD3,
#              uniform sampler2D tex_0 : TEXUNIT0,
#              uniform sampler2D k_Ldepthmap : TEXUNIT1,
#              uniform float4 k_ambient,
# 	     uniform float4 k_texDisable,
#              out float4 o_color:COLOR)
# {
#   float3 circleoffs = float3(l_lightclip.xy / l_lightclip.w, 0);
#   float falloff = saturate(1.0 - dot(circleoffs, circleoffs));
#   float4 baseColor = saturate(tex2D(tex_0, l_texcoord0) + k_texDisable);
#   float shade = tex2Dproj(k_Ldepthmap,l_shadowcoord);
#
#   /***** this is the only line that has changed *****/
#   o_color = baseColor * ( falloff * shade * l_smooth + (1.0-falloff)*l_smooth + k_ambient.x );
# }
