from GamePlusEditor.ursina import *
from panda3d.core import StencilAttrib,CardMaker,ColorWriteAttrib

class CodeEditorUrsaVisor(Entity):
    '''A visual code editor, code by just drag'n droping the code blocks'''
    def __init__(self,EditorDataDict,CodeBlocks = [],**kwargs):
        super().__init__()
        self.CodeBlocks = CodeBlocks
        self.PosSnapping = 0.004
        self.ScaleSnapping = 100    
        self.EditorDataDict = EditorDataDict

        self.UniversalParentEntity = Entity(parent = camera.ui,enabled = kwargs["enabled"])

        self.CodeBlocksMenuParentEntity = Button(name = "EveryItemMenuParentEntity",parent = self.UniversalParentEntity,model = "cube",NotRotateOnHover = True,color = color.tint(color.black,.1),scale = Vec3(0.625005, 0.446007, 1),position = Vec3(-0.571996, -0.27, 1),render_queue  = -2)

        self.RotateWorldButton = Button(parent = self.UniversalParentEntity,color = color.clear,radius=0,position = Vec3(-0.571996, 0.197, 0),rotation = Vec3(0, 0, 0),scale = Vec3(0.628005, 0.475007, 1),render_queue  = -1)

        self.CodeBlockGraph = Button(name = "Text field", parent = self.UniversalParentEntity,model = "cube",NotRotateOnHover = True,position = Vec3(0, 0, 20),rotation = Vec3(0, 0, 0),scale = Vec3(1000,1000, 1),color = color.white,texture = "white_cube",render_queue  = -3)

        self.PosText = Text(parent = self.UniversalParentEntity,name  = "Texte",text = f"({round(self.CodeBlockGraph.x,2)},{round(self.CodeBlockGraph.y,2)})", position = Vec3(0.874992, 0.480997, -20),rotation = Vec3(0, 0, 0),scale = Vec3(1, 1, 1),always_on_top = True,origin = (.5,.5))

        self.CodeBlockGraph.texture_scale = (10000,10000)
        self.constantOneStencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOZero, StencilAttrib.SOReplace, StencilAttrib.SOReplace, 1, 0, 1)
        self.stencilReader = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, 1, 0)

        self.temp = Button(name = "EveryItemMenuParentEntity",parent = self.CodeBlockGraph,model = "cube",NotRotateOnHover = True,color = color.black,scale = Vec3(0.001, 0.001, 1),position = Vec3(0,0,0),render_queue  = -3)

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

        self.PosText.text = f"({round(self.CodeBlockGraph.x,1)},{round(self.CodeBlockGraph.y,1)})"
        return
        # print(self.CodeBlockGraph.scale)
    
    def input(self,key):
        if key == "up arrow":
            self.PosSnapping += 0.001
            return
        elif key == "down arrow":
            self.PosSnapping -= 0.001
            return
        elif key == "up arrow" and held_keys["shift"]:
            self.PosSnapping += 10
            return
        elif key == "down arrow" and held_keys["shift"]:
            self.PosSnapping -= 10
            return

        elif key == "left arrow":
            self.CodeBlockGraph.scale = (self.CodeBlockGraph.scale_x - self.ScaleSnapping /self.CodeBlockGraph.scale_x + self.ScaleSnapping,self.CodeBlockGraph.scale_x - self.ScaleSnapping/self.CodeBlockGraph.scale_y + self.ScaleSnapping,1)
            return

        elif key == "right arrow":
            self.CodeBlockGraph.scale =  (self.CodeBlockGraph.scale_x + self.ScaleSnapping /self.CodeBlockGraph.scale_x - self.ScaleSnapping ,self.CodeBlockGraph.scale_y + self.ScaleSnapping /self.CodeBlockGraph.scale_x - self.ScaleSnapping ,1)
            return

        elif key == "o" and held_keys["control"]:
            self.CodeBlockGraph.x = 0
            self.CodeBlockGraph.y = 0
            return

        elif key == "r" and held_keys["control"]:
            self.PosSnapping = 0.004
            return

    def SetUp(self):
        self.AddStencilToBlocks(self.CodeBlockGraph)

        self.ConfigEditorAsSettings(self.EditorDataDict)

    def ConfigEditorAsSettings(self,DataDict):
        self.SetTooltip(DataDict["Show tooltip"])

    def SetTooltip(self,value):
        self.ItemToToolTipList = []
        if value:
            self.ToolTipList = []
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = Tooltip(self.ToolTipList[i],z = -30,render_queue = 3,always_on_top = True)
                # self.ItemToToolTipList[i].tool_tip.background.z = -1

        else:
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = None

    def SaveEditor(self):
        print(f"{__file__}:: helo")
        

if __name__ == "__main__":
    from GamePlusEditor.ProjectEditor import ProjectEditor
    app = Ursina()
    ed = EditorCamera()
    project = ProjectEditor(Func(print,"yeah"),CurrentTabs=[],EditorCamera=ed)
    editor = CodeEditorUrsaVisor(enabled=True)
    Entity(model  = "cube",texture = "white_cube")
    # editor.model = "cube"
    Sky()

    left = .001
    right = .001
    top = .001
    bottom = .001
    editor.AddStencilToBlocks(editor.CodeBlockGraph)
    editor.MakeEditorEnvironment(application.base.camNode,(125,125,124,0),(0.0019, 0.355, 0.4599 ,0.935))

    ToEdit = editor.PosText

    # def input(key):
    #     global top,bottom,left,right
    #     if key in ["up arrow","up arrow hold"] and not held_keys["shift"]:
    #         # top += .001
    #         ToEdit.y += top
    #     elif key in ["down arrow","down arrow hold"] and not held_keys["shift"]:
    #         # bottom += .001
    #         ToEdit.y -= top
    #     elif key in ["left arrow","left arrow hold"] and not held_keys["shift"]:
    #         # left += .001
    #         ToEdit.x -= top
    #     elif key in ["right arrow","right arrow hold"] and not held_keys["shift"]:
    #         # right += .001
    #         # editor.cm.setFrame(right,left,bottom,top)
    #         ToEdit.x += top


    #     if key in ["r","r hold"] and not held_keys["shift"]:
    #         # top += .001
    #         ToEdit.scale_y += top
    #     elif key in ["t","t hold"] and not held_keys["shift"]:
    #         # bottom += .001
    #         ToEdit.scale_x += top

    #     elif key in ["r","r hold"] and held_keys["shift"]:
    #         # left += .001
    #         ToEdit.scale_y -= top
    #     elif key in ["t","t hold"] and held_keys["shift"]:
    #         # right += .001
    #         # editor.cm.setFrame(right,left,bottom,top)
    #         ToEdit.scale_x -= top


    #     elif key == "p":
    #         editor.PrintItemStatTemp(editor.UniversalParentEntity)

    # def update():
    #     try:
    #         print(mouse.hovered_entity.name)
    #     except:
    #         ...
    project.CurrentTabs.append(editor)
    # project.TopButtonsParentEntity.color = color.clear
    app.run()

