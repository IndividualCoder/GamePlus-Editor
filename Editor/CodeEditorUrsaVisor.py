from ursina import *
from panda3d.core import StencilAttrib,CardMaker,ColorWriteAttrib
class CodeEditorPython(Entity):
    def __init__(self,CodeBlocks = [],**kwargs):
        super().__init__()
        self.CodeBlocks = CodeBlocks
        self.PosSnapping = 0.001

        self.UniversalParentEntity = Entity(parent = camera.ui,enabled = kwargs["enabled"])

        self.CodeBlocksMenuParentEntity = Button(name = "EveryItemMenuParentEntity",parent = self.UniversalParentEntity,model = "cube",NotRotateOnHover = True,color = color.black,scale = Vec3(0.625005, 0.446007, 1),position = Vec3(-0.571996, -0.27, 1),render_queue  = -2)

        self.RotateWorldButton = Button(parent = self.UniversalParentEntity,color = color.clear,radius=0,position = Vec3(-0.571996, 0.197, 0),rotation = Vec3(0, 0, 0),scale = Vec3(0.628005, 0.475007, 1),render_queue  = -1)

        self.CodeBlockGraph = Button(name = "Text field", parent = self.UniversalParentEntity,model = "cube",NotRotateOnHover = True,position = Vec3(0.314997, -0.028998, 20),rotation = Vec3(0, 0, 0),scale = Vec3(1000,1000, 1),color = color.white,texture = "white_cube",render_queue  = -3)

        self.CodeBlockGraph.texture_scale = (10000,10000)
        self.constantOneStencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOZero, StencilAttrib.SOReplace, StencilAttrib.SOReplace, 1, 0, 1)
        self.stencilReader = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, 1, 0)


        self.cm = CardMaker("cardmaker")
        self.cm.setFrame(-.25,.882,-.49,.433)


        self.viewingSquare = render.attachNewNode(self.cm.generate())
        self.viewingSquare.reparentTo(camera.ui)
        self.viewingSquare.setPos(Vec3(0,0,5))

        self.viewingSquare.node().setAttrib(self.constantOneStencil)
        self.viewingSquare.node().setAttrib(ColorWriteAttrib.make(0))

        self.viewingSquare.setBin('background', 0)
        self.viewingSquare.setDepthWrite(0)

    def AddStencilToBlocks(self,Block):
        # for i in range(len(self.CodeBlocks)):
        Block.node().setAttrib(self.stencilReader)
        print(Block.node().getAttrib(0))

        # self.CodeBlockGraph.node().setAttrib(self.stencilReader)

        # self.CodeWriter.line_numbers.enable()

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


    def update(self):
        if held_keys["w"]:
            self.CodeBlockGraph.y -= self.PosSnapping
        if held_keys["s"]:
            self.CodeBlockGraph.y += self.PosSnapping
        if held_keys["a"]:
            self.CodeBlockGraph.x += self.PosSnapping
        if held_keys["d"]:
            self.CodeBlockGraph.x -= self.PosSnapping


    def input(self,key):
        if key == "up arrow":
            self.PosSnapping += 0.001
        elif key == "down arrow":
            self.PosSnapping -= 0.001

if __name__ == "__main__":
    from ProjectEditor import ProjectEditor
    app = Ursina()
    ed = EditorCamera()
    project = ProjectEditor(Func(print,"yeah"),CurrentTabs=[],EditorCamera=ed)
    editor = CodeEditorPython(enabled=True)
    Entity(model  = "cube",texture = "white_cube")
    # editor.model = "cube"
    Sky()
    left = .001
    right = .001
    top = .001
    bottom = .001
    editor.AddStencilToBlocks(editor.CodeBlockGraph)
    editor.MakeEditorEnvironment(application.base.camNode,(125,125,124,0),(0.0019, 0.355, 0.4599 ,0.935))
    # def input(key):
    #     global top,bottom,left,right
    #     if key in ["w","w hold"] and not held_keys["shift"]:
    #         # top += .001
    #         editor.RotateWorldButton.y += top
    #     elif key in ["s","s hold"] and not held_keys["shift"]:
    #         # bottom += .001
    #         editor.RotateWorldButton.y -= top
    #     elif key in ["a","a hold"] and not held_keys["shift"]:
    #         # left += .001
    #         editor.RotateWorldButton.x -= top
    #     elif key in ["d","d hold"] and not held_keys["shift"]:
    #         # right += .001
    #         # editor.cm.setFrame(right,left,bottom,top)
    #         editor.RotateWorldButton.x += top


    #     if key in ["r","r hold"] and not held_keys["shift"]:
    #         # top += .001
    #         editor.RotateWorldButton.scale_y += top
    #     elif key in ["t","t hold"] and not held_keys["shift"]:
    #         # bottom += .001
    #         editor.RotateWorldButton.scale_x += top

    #     elif key in ["r","r hold"] and held_keys["shift"]:
    #         # left += .001
    #         editor.RotateWorldButton.scale_y -= top
    #     elif key in ["t","t hold"] and held_keys["shift"]:
    #         # right += .001
    #         # editor.cm.setFrame(right,left,bottom,top)
    #         editor.RotateWorldButton.scale_x -= top


    #     elif key == "p":
    #         editor.PrintItemStatTemp(editor.UniversalParentEntity)

    # def update():
    #     try:
    #         print(mouse.hovered_entity.name)
    #     except:
    #         ...
    project.CurrnetTabs.append(editor)
    app.run()

