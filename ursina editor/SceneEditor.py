from ursina import *

class SceneEditor(Entity):
    def __init__(self):
        
        self.TopButtonsParentEntity = Entity(parent = camera.ui)

        
        self.SaveProjectButton = Draggable(parent = self.TopButtonsParentEntity,text="Save",color = color.blue,radius  = 0,position =(-0.793, 0.47, 0),scale = Vec3(0.179, 0.0385, 1))


        self.ShowPosTempButton = Button(Key="p",on_key_press=self.ShowPosTemp,on_click = self.ShowPosTemp,scale= (0.1,0.1))

    def ShowPosTemp(self):
        for i in range(len(self.TopButtonsParentEntity.children)):
            print(self.TopButtonsParentEntity.children[i].position)
            print(self.TopButtonsParentEntity.children[i].scale)

if __name__ == "__main__":
    from OtherStuff import *
    app = Ursina()
    window.fps_counter.disable()
    window.exit_button.disable()
    editor = SceneEditor()
    app.run()

    # ScaleTransformer(editor.SaveProjectButton,.01,1)
    # Button(Key="o",on_key_press=Func(editor.SaveProjectButton.fit_to_text),scale = (0,0))
    # asdf = Button(Key="f",scale = (0,0))
    # def OOOO():
    #     editor.SaveProjectButton.radius = 0
    # asdf.on_key_press = OOOO

