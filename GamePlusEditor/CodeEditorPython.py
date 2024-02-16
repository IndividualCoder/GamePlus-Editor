from GamePlusEditor.ursina import *
from GamePlusEditor.FileSystem.FileMenu import FileMenu
from GamePlusEditor.OtherStuff import CurrentFolderNameReturner
from GamePlusEditor.ursina.color import tint

class CodeEditorPython(Entity):
    '''Main code editor, code with writing word by word. Mainly used to code in python but can code in any language'''
    def __init__(self,EditorDataDict,ShowInstructionFunc,SaveFunction,OnFileAdded,ProjectName = None,UdSrc = [],**kwargs):
        super().__init__()

        self.EditorDataDict = EditorDataDict
        self.Save = SaveFunction
        self.ShowInstructionFunc = ShowInstructionFunc
        self.ReplacementColors = {"class ":    "☾orange☽class ☾default☽",
                                  "def ": "☾rgb(50,50,255)☽def ☾default☽",
                                  "self": "☾yellow☽self☾default☽",
                                  "__init__": "☾rgb(50,150,150)☽__init__☾default☽",
                                  "(":"☾rgb(150, 0, 150)☽(☾default☽",
                                  ")":"☾rgb(150, 0, 150)☽)☾default☽",
                                  "[":"☾rgb(150, 0, 150)☽[☾default☽",
                                  "]":"☾rgb(150, 0, 150)☽]☾default☽",
                                  "{":"☾rgb(150, 0, 150)☽{☾default☽",
                                  "}":"☾rgb(150, 0, 150)☽}☾default☽",}


        self.UniversalParentEntity = Entity(parent = camera.ui,enabled = kwargs["enabled"])

        self.EveryItemMenuParentEntity = Button(name = "EveryItemMenuParentEntity",parent = self.UniversalParentEntity,model = "cube",color = color.tint(color.black,.1),scale = Vec3(0.625005, 0.446007, 1),position = Vec3(-0.571996, -0.27, 0),NotRotateOnHover = True)

        self.CodeWriter = TextField(name = "Text field", parent = self.UniversalParentEntity,active = False,position = Vec3(-0.254003, 0.435, 0),rotation = Vec3(0, 0, 0),scale = Vec3(1, 1, 1),register_mouse_input = True,NotRotateOnHover = True,render_queue = -3)
        self.CodeWriter.line_numbers.enable()
        self.CodeWriter.line_numbers.render_queue = self.CodeWriter.render_queue
        # self.CodeWriter.line_numbers_background.enable()

        self.FileMenu = FileMenu(ProjectName=ProjectName,CodeEditorEntity=self.CodeWriter,Path=f"{CurrentFolderNameReturner()}/Current Games",parent = self.EveryItemMenuParentEntity,queue = 0,z = -10,UdSrc = UdSrc,ShowInstructionFunc = ShowInstructionFunc,OnFileAdded = OnFileAdded)


    def MakeEditorEnvironment(self,cam,color,size):
        '''Changes the camera display region and sets the base color'''
        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0]/255,color[1]/255,color[2]/255,color[3]/255)

    def SetUp(self):
        '''Sets up the class'''
        self.FileMenu.SetUp()
        self.FileMenu.Show()
        self.ConfigEditorAsSettings(self.EditorDataDict)
        self.CodeWriter.replacements = self.ReplacementColors

    def ConfigEditorAsSettings(self,DataDict: dict):
        '''Configures editor as desired setting'''
        self.SetTooltip(DataDict["Show tooltip"])

    def SetTooltip(self,value: bool):
        '''Toogles tooltip as the value'''
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
    from GamePlusEditor.ProjectEditor import ProjectEditor
    from GamePlusEditor.OpenFile import OpenFile
    app = Ursina()
    ed = EditorCamera()
    false = False
    true = True
    project = ProjectEditor(Func(print,"yeah"),CurrentTabs=[],EditorCamera=ed,PlayFunction=Func(print,"hi"),ReadyToHostProjectFunc=Func(print,"hi"),HostProjectFunc=Func(print,"hi"),EditorDataDict={"Show tooltip": true, "Auto save on exit": false, "Show memory counter": true, "Fullscreen": false, "Anti-aliasing sample": 4, "Render distance (near)": 0.1, "Render distance (far)": 10000.0},ShowInstructionFunc=Func(print,"hi"))

    ConfiableEditorDataDefault = {"Show tooltip":True,"Auto save on exit": False,"Show memory counter": True,"Fullscreen": False,"Anti-aliasing sample": 4,"Render distance (near)": .10,"Render distance (far)": 10000.0,}

    ConfiableEditorData = OpenFile("Configable editor data.txt",f"{CurrentFolderNameReturner()}/Editor data",ConfiableEditorDataDefault,True)

    editor = CodeEditorPython(enabled=True,EditorDataDict=ConfiableEditorData,ProjectName="jh",ShowInstructionFunc=Func(print,"hi"),OnFileAdded=Func(print,"hi"),SaveFunction=Func(print,"hi"))

    editor.SetUp()
    # editor.model = "cube"
    Sky()
    left = .001
    right = .001
    top = .001
    bottom = .001
    editor.MakeEditorEnvironment(application.base.camNode,(125,125,124,0),(0.0019, 0.355, 0.4599 ,0.935))

    project.CurrentTabs.append(editor)
    app.run()

