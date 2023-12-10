from ursina import *
from FileSystem.FileMenu import FileMenu
from OtherStuff import CurrentFolderNameReturner
from ursina.color import tint

class CodeEditorPython(Entity):
    '''Main code editor, code with writing word by word. Mainly used to code in python but can code in any language'''
    def __init__(self,EditorDataDict,ShowInstructionFunc,SaveFunction,OnFileAdded,ProjectName = None,UdSrc = [],**kwargs):
        super().__init__()

        self.EditorDataDict = EditorDataDict
        self.Save = SaveFunction
        self.ShowInstructionFunc = ShowInstructionFunc

        self.UniversalParentEntity = Entity(parent = camera.ui,enabled = kwargs["enabled"])

        self.EveryItemMenuParentEntity = Button(name = "EveryItemMenuParentEntity",parent = self.UniversalParentEntity,model = "cube",color = color.tint(color.black,.1),scale = Vec3(0.625005, 0.446007, 1),position = Vec3(-0.571996, -0.27, 0),NotRotateOnHover = True)

        self.CodeWriter = TextField(name = "Text field", parent = self.UniversalParentEntity,active = False,position = Vec3(-0.254003, 0.435, 0),rotation = Vec3(0, 0, 0),scale = Vec3(1, 1, 1),register_mouse_input = True,NotRotateOnHover = True,render_queue = -3)
        self.CodeWriter.line_numbers.enable()
        self.CodeWriter.line_numbers.render_queue = self.CodeWriter.render_queue
        # self.CodeWriter.line_numbers_background.enable()

        self.FileMenu = FileMenu(ProjectName=ProjectName,CodeEditorEntity=self.CodeWriter,Path=f"{CurrentFolderNameReturner()}/Current Games",parent = self.EveryItemMenuParentEntity,queue = 0,z = -10,UdSrc = UdSrc,ShowInstructionFunc = ShowInstructionFunc,OnFileAdded = OnFileAdded)


    def MakeEditorEnvironment(self,cam,color,size):

        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0]/255,color[1]/255,color[2]/255,color[3]/255)

    def PrintItemStatTemp(self,Entity):
        for i in range(len(Entity.children)):
            print(f"name: {Entity.children[i].name} position = {Entity.children[i].position},rotation = {Entity.children[i].rotation},scale = {Entity.children[i].scale}")
            if len(Entity.children[i].children) > 0:
                self.PrintItemStatTemp(Entity.children[i])

    def SetUp(self):
        self.FileMenu.SetUp()
        self.FileMenu.Show()
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
        self.FileMenu.SaveCurrentFile()
        self.Save()


if __name__ == "__main__":
    from ProjectEditor import ProjectEditor
    from OpenFile import OpenFile
    app = Ursina()
    ed = EditorCamera()

    project = ProjectEditor(Func(print,"yeah"),CurrentTabs=[],EditorCamera=ed,PlayFunction=Func(print,"hi"),ReadyToHostProjectFunc=Func(print,"hi"),HostProjectFunc=Func(print,"hi"))

    ConfiableEditorDataDefault = {"Show tooltip":True,"Auto save on exit": False,"Show memory counter": True,"Fullscreen": False,"Anti-aliasing sample": 4,"Render distance (near)": .10,"Render distance (far)": 10000.0,}

    ConfiableEditorData = OpenFile("Configable editor data.txt",f"{CurrentFolderNameReturner()}/Editor data",ConfiableEditorDataDefault,True)

    editor = CodeEditorPython(enabled=True,EditorDataDict=ConfiableEditorData,ProjectName="jh")
    editor.SetUp()
    # editor.model = "cube"
    Sky()
    left = .001
    right = .001
    top = .001
    bottom = .001
    editor.MakeEditorEnvironment(application.base.camNode,(125,125,124,0),(0.0019, 0.355, 0.4599 ,0.935))
    # def input(key):
    #     global top,bottom,left,right
    #     if key in ["w","w hold"] and not held_keys["shift"]:
    #         # top += .001

    #         editor.CodeWriter.y += top
    #     elif key in ["s","s hold"] and not held_keys["shift"]:
    #         # bottom += .001
    #         editor.CodeWriter.y -= top
    #     elif key in ["a","a hold"] and not held_keys["shift"]:
    #         # left += .001
    #         editor.CodeWriter.x -= left
    #     elif key in ["d","d hold"] and not held_keys["shift"]:
    #         # right += .001
    #         editor.CodeWriter.x += left

    #     elif key in ["r","r hold"] and not held_keys["shift"]:
    #         # left += .001
    #         editor.CodeWriter.scale_x += left
    #     elif key in ["t","t hold"] and not held_keys["shift"]:
    #         # right += .001
    #         editor.CodeWriter.scale_y += left

    #     elif key in ["r","r hold"] and held_keys["shift"]:
    #         # left += .001
    #         editor.CodeWriter.scale_x -= left
    #     elif key in ["t","t hold"] and held_keys["shift"]:
    #         # right += .001
    #         editor.CodeWriter.scale_y -= left

    #     elif key == "p":
    #         editor.PrintItemStatTemp(editor.UniversalParentEntity)
            

    project.CurrentTabs.append(editor)
    app.run()
