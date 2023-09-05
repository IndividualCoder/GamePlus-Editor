from ursina import *

class CodeEditorPython(Entity):
    def __init__(self,**kwargs):
        super().__init__()

        self.UniversalParentEntity = Entity(parent = camera.ui,enabled = kwargs["enabled"])

        self.EveryItemMenuParentEntity = Button(name = "EveryItemMenuParentEntity",parent = self.UniversalParentEntity,model = "cube",color = color.white,scale = Vec3(0.625005, 0.446007, 1),position = Vec3(-0.571996, -0.27, 0),NotRotateOnHover = True)

        self.CodeWriter = TextField(name = "Text field", parent = self.UniversalParentEntity,active = False,position = Vec3(-0.254003, 0.435, 0),rotation = Vec3(0, 0, 0),scale = Vec3(1, 1, 1),register_mouse_input = True,NotRotateOnHover = True)
        self.CodeWriter.line_numbers.enable()
        # self.CodeWriter.line_numbers_background.enable()

    def MakeEditorEnvironment(self,cam,color,size):

        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0]/255,color[1]/255,color[2]/255,color[3]/255)

    def PrintItemStatTemp(self,Entity):
        for i in range(len(Entity.children)):
            print(f"name: {Entity.children[i].name} position = {Entity.children[i].position},rotation = {Entity.children[i].rotation},scale = {Entity.children[i].scale}")
            if len(Entity.children[i].children) > 0:
                self.PrintItemStatTemp(Entity.children[i])

if __name__ == "__main__":
    from ProjectEditor import ProjectEditor
    app = Ursina()
    ed = EditorCamera()
    project = ProjectEditor(Func(print,"yeah"),CurrentTabs=[],EditorCamera=ed)
    editor = CodeEditorPython(enabled=True)
    # editor.model = "cube"
    Sky()
    left = .001
    right = .001
    top = .001
    bottom = .001
    editor.MakeEditorEnvironment(application.base.camNode,(125,125,124,0),(0.0019, 0.355, 0.4599 ,0.935))
    def input(key):
        global top,bottom,left,right
        if key in ["w","w hold"] and not held_keys["shift"]:
            # top += .001

            editor.CodeWriter.y += top
        elif key in ["s","s hold"] and not held_keys["shift"]:
            # bottom += .001
            editor.CodeWriter.y -= top
        elif key in ["a","a hold"] and not held_keys["shift"]:
            # left += .001
            editor.CodeWriter.x -= left
        elif key in ["d","d hold"] and not held_keys["shift"]:
            # right += .001
            editor.CodeWriter.x += left

        elif key in ["r","r hold"] and not held_keys["shift"]:
            # left += .001
            editor.CodeWriter.scale_x += left
        elif key in ["t","t hold"] and not held_keys["shift"]:
            # right += .001
            editor.CodeWriter.scale_y += left

        elif key in ["r","r hold"] and held_keys["shift"]:
            # left += .001
            editor.CodeWriter.scale_x -= left
        elif key in ["t","t hold"] and held_keys["shift"]:
            # right += .001
            editor.CodeWriter.scale_y -= left

        elif key == "p":
            editor.PrintItemStatTemp(editor.UniversalParentEntity)
            

    project.CurrentTabs.append(editor)
    app.run()

