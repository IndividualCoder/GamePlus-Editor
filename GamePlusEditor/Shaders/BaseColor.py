from GamePlusEditor.ursina import *

BaseColorShaderVert = '''
#version 150

uniform mat4 p3d_ModelViewProjectionMatrix;

in vec4 p3d_Vertex;

void main()
{
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
'''

BaseColorShaderFrag = '''
#version 150

out vec4 fragColor;
int a = 12;
void main() {
  fragColor = vec4(0, 1, 0, 1);
}
'''
  
BaseColorShader = Shader(vertex=BaseColorShaderVert,fragment=BaseColorShaderFrag)

if __name__ == "__main__":
    import sys
    import os
    # Make the main to 'Editor' so we can access the files of the 'Editor' folder
    editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(editor_directory)

    app = Ursina()

    cube = Entity(model = "cube",shader = BaseColorShader,color = color.red)
    EditorCamera()
    app.run()