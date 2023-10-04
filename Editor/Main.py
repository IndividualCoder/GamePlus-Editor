from ursina import *
from StartingUI import StartingUI
from SceneEditor  import SceneEditor
from ProjectSaver import ProjectSaver
from OtherStuff import FormatForSaving,CurrentFolderNameReturner,RecursivePerformer
import os
from OpenFile import OpenFile,SaveFile
from ursina.prefabs.memory_counter import MemoryCounter
from CoreFiles.InstructionMenu import InstructionMenu
from ursina.color import tint
from ProjectExporter import ProjectExporter
from ProjectEditor import ProjectEditor
from CodeEditorPython import CodeEditorPython
from CodeEditorUrsaVisor import CodeEditorUrsaVisor
import atexit
from panda3d.core import *
from direct.filter.CommonFilters import CommonFilters


class UrsinaEditor(Entity):
    def __init__(self,EditorCamera,**kwargs):
        super().__init__()
        self.CurrentSupportedEditors = ["Scene editor","Code editor","Ursa-visor editor"]
        self.AddCurrentSupportedEditors = [self.AddSceneEditor,self.AddPythonCodeEditor,self.AddUrsaVisorEditor]
        self.ProjectEditorsList = []
        self.CurrentProjectEditor: ProjectEditor = None


        self.EditorCamera = EditorCamera
        self.NonConfiableEditorDataDefault = {"CurrentProjectNames": []}
        self.NonConfiableEditorData = OpenFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorDataDefault,True)
        self.InstructionList = []

        self.ConfiableEditorDataDefault = {"Show tooltip":True,"Auto save on exit": False,"Show memory counter": True,"Fullscreen": False,"Anti-aliasing sample": 4,"Render distance (near)": .10,"Render distance (far)": 10000.0,}
        self.ConfiableEditorDataDefaultType = ("bool","bool","bool","bool","int","float","float")
        self.ConfiableEditorData = OpenFile("Configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.ConfiableEditorDataDefault,True)
        self.FolderName = os.path.dirname(os.path.abspath(__file__))
        self.RecentEdits = ["",""]
        self.ProjectSettings = None
        self.Filter = CommonFilters(base.win, base.cam)

        self.MemoryCounter = MemoryCounter(enabled=self.ConfiableEditorData["Show memory counter"])
        self.StartingUi = StartingUI(EditorDataDict=  self.ConfiableEditorData,OnProjectStart=self.StartEdit,ExistingProjectsName=self.NonConfiableEditorData["CurrentProjectNames"],ChangeConfigDataToDefaultTypeFunc=self.ChangeConfigDataToDefaultType,ProjectName="",SaveNonConfiableData=self.SaveData,ShowInstructionFunc = self.ShowInstruction)
        # self.StartingUi.ShowRecentProjects()

        # self.StartingUi.RecentProjectsScrollerParentEntity.= len(self.StartingUi.TotalRunningProjects)

    def StartEdit(self):
        self.ProjectEditorsList.append(ProjectEditor(ExportToPyFunc=self.ExportProjectToPy,CurrentTabs=[],EditorCamera=self.EditorCamera,enabled = True,ToAddTabsText=self.CurrentSupportedEditors,ToAddTabsFunc=self.AddCurrentSupportedEditors,PlayFunction=self.PlayProject))
        self.CurrentProjectEditor: ProjectEditor = self.ProjectEditorsList[-1]
        self.CurrentProjectEditor.SetUp()
        self.CurrentProjectEditor.ProjectName = self.StartingUi.ProjectName
        self.CurrentProjectEditor.ProjectSettings = self.StartingUi.ProjectSettings
        self.StartingUi.ProjectName = ""
        self.StartingUi.ProjectSettings = {"ProjectGraphicsQuality": "Low","ProjectLanguage": "Python","ProjectNetworkingOnline": False,"CurrentTargatedPlatform": "windows","CurrentProjectBase": "FPC"}
        self.AddSceneEditor()
        self.CurrentProjectEditor.JumpTabs(0)

        # self.ProjectEditor.UpdateTabsMenu()
        self.EditorCamera.item_to_in_find_on_mouse_hit_rotate = self.CurrentProjectEditor.CurrentSceneEditor.WorldItems

        self.CurrentProjectEditor.CurrentSceneEditor.enable()
        self.CurrentProjectEditor.CurrentSceneEditor.UniversalParentEntity.enable()
        RecursivePerformer(self.CurrentProjectEditor.CurrentSceneEditor.UniversalParentEntity)
        # self.Editor.Tempa.enable()
        # self.Editor.ignore = False


    def SetupEditor(self,Editor):
        if Editor.name.startswith("Scene"):
            Editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, .999, 0.1009, 0.938))
        elif Editor.name.startswith("Code"):
            Editor.SetUp()
        elif Editor.name.startswith("Ursa"):
            Editor.SetUp()

    def Save(self):
        # self.WorldItems = self.SceneEditor.WorldItems
        # self.ToImport = self.SceneEditor.ToImport
        # print(type(self.WorldItems[0]).__name__)

        ProjectSaver(ProjectName = self.CurrentProjectEditor.ProjectName,UdFunc = self.CurrentProjectEditor.UDFunc,UdVar=self.CurrentProjectEditor.UDVars,Udsrc=self.CurrentProjectEditor.UDSrc,WindowConfig=self.CurrentProjectEditor.UDWindowConfig,ToImport=list(self.CurrentProjectEditor.ToImport),Items = self.CurrentProjectEditor.CurrentSceneEditor.WorldItems,Path=f'{FormatForSaving(self.FolderName)}Current Games',GameSettings=self.CurrentProjectEditor.ProjectSettings)

        if not self.CurrentProjectEditor.ProjectName in self.NonConfiableEditorData["CurrentProjectNames"]:
            self.NonConfiableEditorData["CurrentProjectNames"].append(self.CurrentProjectEditor.ProjectName)
            self.SaveData()

    def SaveOnExit(self):
        if self.ConfiableEditorData["Auto save on exit"] and self.StartingUi.ProjectName:
            self.Save()

    def Setup(self):
        # Register the exit_handler function
        self.ConfigEditorAsSettings()

        atexit.register(self.SaveOnExit)

        self.StartingUi.Setup()
        self.StartingUi.ShowRecentProjects(self.EnableWorldItemsAndSetProjectName)



    def SaveData(self):
        # print("saveing")
        SaveFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorData)
        SaveFile("Configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.ConfiableEditorData)

    def ChangeConfigDataToDefaultType(self,Data: dict):
        try:
            for i,j in enumerate(self.ConfiableEditorDataDefault):
                if type(self.ConfiableEditorDataDefault[j]).__name__ == "int":
                    Data[j] = int(Data[j])

                elif type(self.ConfiableEditorDataDefault[j]).__name__ == "float":
                    if Data[j].find('.') != -1:
                        Data[j] = Data[j][:Data[j].find('.') + 1] + Data[j][Data[j].find('.') + 1:].replace('.', '')
                    Data[j] = float(Data[j])  

                elif type(self.ConfiableEditorDataDefault[j]).__name__ == "bool":
                    if Data[j].lower() == "true":
                        Data[j] = True
                    elif Data[j].lower() == "false":
                        Data[j] = False

                elif type(self.ConfiableEditorDataDefault[j]).__name__ == "str":
                    Data[j] = str(Data[j])

                # self.ConfiableEditorDataDefaultType[i]

            self.ConfiableEditorData = Data
            # print("helo",self.ConfiableEditorData)
            self.ConfigEditorAsSettings()

        except Exception as e:
            print(f"{__file__}:: {e}")


    def ShowInstruction(self,Str,Color = tint(color.white,-.6),Title = "Info",KillIn = 1,KillAfter = 5,WordWrap = 40):
        self.InstructionList.append(InstructionMenu(ToSay=Str,OnXClick=Func(self.DestroyInstruction,Index = -1),Title=Title,DestroyFunc=Func(self.DestroyInstruction,Index = -1),Color=Color,KillIn =KillIn,killAfter=KillAfter,WordWrap=WordWrap))

    def AddSceneEditor(self):
        self.CurrentProjectEditor.CurrentTabs.append(SceneEditor(enabled = True,SaveFunction= self.Save,ShowInstructionFunc = self.ShowInstruction,ExportToPyFunc=self.ExportProjectToPy,EditorCamera = self.EditorCamera))
        # self.CurrentProjectEditor.CurrentEditor = self.CurrentProjectEditor.CurrentTabs[-1]
        # self.CurrentProjectEditor.CurrentEditor = self.CurrentProjectEditor.CurrentTabs[-1]

        self.CurrentProjectEditor.CurrentTabs[-1].name = f"Scene Editor {len([i for i in range(len(self.CurrentProjectEditor.CurrentTabs)) if type(self.CurrentProjectEditor.CurrentTabs[i]).__name__ == 'SceneEditor'])}"
        self.CurrentProjectEditor.CurrentTabs[-1].GetPosTemp()
        self.CurrentProjectEditor.CurrentTabs[-1].Setup()

        if len(self.CurrentProjectEditor.CurrentTabs) > 1:
            self.CurrentProjectEditor.CurrentTabs[-1].WorldItems = self.CurrentProjectEditor.CurrentSceneEditor.WorldItems
            self.CurrentProjectEditor.CurrentTabs[-1].ignore = True
            self.CurrentProjectEditor.CurrentTabs[-1].disable()
            self.CurrentProjectEditor.CurrentTabs[-1].UniversalParentEntity.disable()
            RecursivePerformer(self.CurrentProjectEditor.CurrentTabs[-1].SpecialEntities,"disable")

        else:
            self.CurrentProjectEditor.CurrentSceneEditor:SceneEditor = self.CurrentProjectEditor.CurrentTabs[-1]
            self.CurrentProjectEditor.CurrentEditor = self.CurrentProjectEditor.CurrentTabs[-1]
            self.CurrentProjectEditor.CurrentTabs[-1].enable()
            RecursivePerformer(self.CurrentProjectEditor.CurrentTabs[-1].UniversalParentEntity)
            RecursivePerformer(self.CurrentProjectEditor.CurrentTabs[-1].SpecialEntities)
            self.SetupEditor(self.CurrentProjectEditor.CurrentTabs[-1])

            # destroy(self.StartingUi,delay=2)
            # del self.StartingUi

        self.CurrentProjectEditor.UpdateTabsMenu()


    def AddPythonCodeEditor(self):
        self.CurrentProjectEditor.CurrentTabs.append(CodeEditorPython(ProjectName=self.CurrentProjectEditor.ProjectName,enabled=False,ignore = True))

        self.CurrentProjectEditor.CurrentTabs[-1].name = f"Code Editor {len([i for i in range(len(self.CurrentProjectEditor.CurrentTabs)) if type(self.CurrentProjectEditor.CurrentTabs[i]).__name__ == 'CodeEditorPython'])}" 
        self.SetupEditor(self.CurrentProjectEditor.CurrentTabs[-1])
        self.CurrentProjectEditor.UpdateTabsMenu()

    def AddUrsaVisorEditor(self):
        self.CurrentProjectEditor.CurrentTabs.append(CodeEditorUrsaVisor(enabled=False,ignore = True,ProjectName=self.CurrentProjectEditor.ProjectName))

        self.CurrentProjectEditor.CurrentTabs[-1].name = f"Ursa Editor {len([i for i in range(len(self.CurrentProjectEditor.CurrentTabs)) if type(self.CurrentProjectEditor.CurrentTabs[i]).__name__ == 'CodeEditorUrsaVisor'])}" 

        self.SetupEditor(self.CurrentProjectEditor.CurrentTabs[-1])
        self.CurrentProjectEditor.UpdateTabsMenu()

    def DestroyInstruction(self,Index = None):
        # print("helo")
        for i in range(len(self.InstructionList)):
            # self.InstructionList[i].kill(.2)
            destroy(self.InstructionList[i],delay=.1)

    def ConfigEditorAsSettings(self):
        self.MemoryCounter.enabled = self.ConfiableEditorData["Show memory counter"]
        self.StartingUi.EditorDataDict = self.ConfiableEditorData
        self.StartingUi.ConfigEditorAsSettings()
        window.fullscreen = self.ConfiableEditorData["Fullscreen"]
        camera.clip_plane_near = self.ConfiableEditorData["Render distance (near)"]
        camera.clip_plane_far = self.ConfiableEditorData["Render distance (far)"]
        if self.ConfiableEditorData["Anti-aliasing sample"] > 0:
            self.Filter.delMSAA()
            self.Filter.setMSAA(self.ConfiableEditorData["Anti-aliasing sample"])
        else:
            self.Filter.delMSAA()

    def ExportProjectToPy(self,Path):
        self.Save()
        # self.ToSaveWorldItems = self.SceneEditor.WorldItems
        # self.ToSaveToImport = self.SceneEditor.ToImport
        # self.ToSaveProjectSettings = self.StartingUi.ProjectSettings
        # self.ToSaveProjectName = self.StartingUi.ProjectName
        Path.replace("\\","/")
        Path += "/Exported games"
        print(Path)

        ProjectExporter(ProjectName = self.CurrentProjectEditor.ProjectName,ProjectPath=f'{FormatForSaving(self.FolderName)}Current Games',ToSavePath=Path)
        # print(Path.split("/",-1))
        self.ShowInstruction("Exported successfully")

    def PlayProject(self):
        wp = WindowProperties()
        wp.setSize(960, 540)
        wp.title = self.CurrentProjectEditor.ProjectName
        win2 = base.openWindow(props=wp, aspectRatio=16/9,name = "hi",keepCamera = True)
        dr = win2.makeDisplayRegion()
        dr.sort = 20

        myCamera2d = NodePath(Camera('myCam2d'))
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-1000, 1000)
        myCamera2d.node().setLens(lens)

        myRender2d = NodePath('myRender2d')
        myRender2d.setDepthTest(True)
        myRender2d.setDepthWrite(True)
        myCamera2d.reparentTo(myRender2d)
        dr.setCamera(myCamera2d)
        Button(on_click = Func(print,"hi"))

    def EnableWorldItemsAndSetProjectName(self,WorldItemsList,Projec = ""):
        # self.StartingUi.StartProject()
        self.StartEdit()
        for item in WorldItemsList:
            # Evaluate the class constructor as an expression and append the result to the list
            self.CurrentProjectEditor.CurrentSceneEditor.WorldItems.append(eval(item['cls'] + item['args']))
        self.SetProjectName(Projec)

    def SetProjectName(self,Value: str):
        self.CurrentProjectEditor.ProjectName = Value



if __name__ == "__main__":
    # from panda3d.core import AntialiasAttrib
    
    app = Ursina()
    window.exit_button.disable()
    window.fps_counter.disable()

    Sky()

    Editor = UrsinaEditor(EditCam := EditorCamera()) # the ':=' operator is called walrus operator. google it!  
    Editor.Setup()
    # render.setAntialias(AntialiasAttrib.MAuto)
    app.run()