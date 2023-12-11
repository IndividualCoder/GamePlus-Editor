from GamePlusEditor.ursina import *

BaseColorShaderVert = '''
#version 150

attribute vec3 aPosition;
attribute vec2 aTexCoord;

varying vec2 pos;

void main(){
pos = aTexCoord;
vec4 position = vec4(aPosition, 1.0);
position.xy = position.xy * 2.0 - 1.0;
gl_Position = position;
}
'''

BaseColorShaderFrag = '''
#version 150

void main(){
gl_FragColor = vec4(1.0);
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