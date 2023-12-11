from GamePlusEditor.ursina import *
from GamePlusEditor.StartingUI import StartingUI
from GamePlusEditor.SceneEditor  import SceneEditor
from GamePlusEditor.ProjectSaver import ProjectSaver
from GamePlusEditor.OtherStuff import CurrentFolderNameReturner,RecursivePerformer
import os
from GamePlusEditor.OpenFile import OpenFile,SaveFile
from GamePlusEditor.ursina.prefabs.memory_counter import MemoryCounter
from GamePlusEditor.CoreFiles.InstructionMenu import InstructionMenu
from GamePlusEditor.ursina.color import tint
from GamePlusEditor.ProjectExporter import ProjectExporter
from GamePlusEditor.ProjectEditor import ProjectEditor
from GamePlusEditor.CodeEditorPython import CodeEditorPython
from GamePlusEditor.CodeEditorUrsaVisor import CodeEditorUrsaVisor
import atexit
from direct.filter.CommonFilters import CommonFilters
from GamePlusEditor.CoreFiles.InstructionList import InstructionList
import socket
import subprocess
from GamePlusEditor.CoreFiles.Terminal import Terminal

class UrsinaEditor(Entity):
    def __init__(self,EditorCamera,**kwargs):
        super().__init__()
        self.CurrentSupportedEditors = ["Scene editor","Code editor","Ursa-visor editor"]
        self.AddCurrentSupportedEditors = [self.AddSceneEditor,self.AddPythonCodeEditor,self.AddUrsaVisorEditor]
        self.ProjectEditorsList = []
        self.CurrentProjectEditor: ProjectEditor = None
        self.CurrentTerminals = []

        self.EditorCamera = EditorCamera
        self.NonConfiableEditorDataDefault = {"CurrentProjectNames": [],"RecentEdits": []}
        self.NonConfiableEditorData = OpenFile("Non configable editor data.txt",f"{CurrentFolderNameReturner()}/Editor data",self.NonConfiableEditorDataDefault,True)
        self.InstructionList = InstructionList()

        self.ConfiableEditorDataDefault = {"Show tooltip":True,"Auto save on exit": False,"Show memory counter": True,"Fullscreen": False,"Anti-aliasing sample": 4,"Render distance (near)": .10,"Render distance (far)": 10000.0,}
        self.ConfiableEditorDataDefaultType = ("bool","bool","bool","bool","int","float","float")
        self.ConfiableEditorData = OpenFile("Configable editor data.txt",f"{CurrentFolderNameReturner()}/Editor data",self.ConfiableEditorDataDefault,True)
        self.FolderName = os.path.dirname(os.path.abspath(__file__))
        self.ProjectSettings = None
        self.Filter = CommonFilters(base.win, base.cam)

        self.MemoryCounter = MemoryCounter(enabled=self.ConfiableEditorData["Show memory counter"])
        self.StartingUi = StartingUI(EditorDataDictConfigable=  self.ConfiableEditorData,RegiveDataDictFunc = self.RetakeDataDict,RetakeDataDictFunc=self.RegiveDataDict,EditorDataDictNonConfigable = self.NonConfiableEditorData,OnProjectStart=self.StartEdit,ChangeConfigDataToDefaultTypeFunc=self.ChangeConfigDataToDefaultType,ProjectName="",SaveNonConfiableData=self.SaveData,FuncToEnableOnOpen=self.EnableWorldItemsAndSetProjectName,ShowInstructionFunc = self.ShowInstruction,RemoveProjectNameFunc = self.RemoveProject,ExportToPyFunc = self.ExportProjectToPy)


    def StartEdit(self):
        self.ProjectEditorsList.append(ProjectEditor(ExportToPyFunc=self.ExportProjectToPy,CurrentTabs=[],ShowInstructionFunc=self.ShowInstruction,EditorCamera=self.EditorCamera,ReadyToHostProjectFunc=self.ReadyToHostProject,HostProjectFunc=self.HostProject,enabled = True,ToAddTabsText=self.CurrentSupportedEditors,ToAddTabsFunc=self.AddCurrentSupportedEditors,PlayFunction=self.PlayProject))
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


    def SetupEditor(self,Editor):
        if Editor.name.startswith("Scene"):
            Editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, .999, 0.1009, 0.938))
        elif Editor.name.startswith("Code"):
            Editor.SetUp()
        elif Editor.name.startswith("Ursa"):
            Editor.SetUp()

    def Save(self):
        ProjectSaver(ProjectName = self.CurrentProjectEditor.ProjectName,UdFunc = self.CurrentProjectEditor.UDFunc,UdVar=self.CurrentProjectEditor.UDVars,Udsrc=self.CurrentProjectEditor.UDSrc,WindowConfig=self.CurrentProjectEditor.UDWindowConfig,ToImport=list(self.CurrentProjectEditor.ToImport),Items = self.CurrentProjectEditor.CurrentSceneEditor.WorldItems,Path=f'{self.FolderName}/Current Games',GameSettings=self.CurrentProjectEditor.ProjectSettings)

        if not self.CurrentProjectEditor.ProjectName in self.NonConfiableEditorData["CurrentProjectNames"]:
            self.NonConfiableEditorData["CurrentProjectNames"].append(self.CurrentProjectEditor.ProjectName)
            self.SaveData()

    def OnExit(self):
        if self.ConfiableEditorData["Auto save on exit"] and self.StartingUi.ProjectName:
            self.Save()
    def Setup(self):
        # Register the exit_handler function
        self.ConfigEditorAsSettings()

        atexit.register(self.OnExit)

        self.StartingUi.Setup()
        self.StartingUi.ShowRecentProjects(self.EnableWorldItemsAndSetProjectName)

    def  SaveData(self):
        # print("saveing")
        SaveFile("Non configable editor data.txt",f"{CurrentFolderNameReturner()}/Editor data",self.NonConfiableEditorData)
        SaveFile("Configable editor data.txt",f"{CurrentFolderNameReturner()}/Editor data",self.ConfiableEditorData)

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
        self.InstructionList.append(InstructionMenu(ToSay=Str,Title=Title,Color=Color,KillIn =KillIn,killAfter=KillAfter,WordWrap=WordWrap))
        self.InstructionList[-1].CloseButton.on_click = Func(self.DestroyInstruction,self.InstructionList[-1])

    def DestroyInstruction(self,Instruction):
        self.Index = self.InstructionList.index(Instruction)
        destroy(self.InstructionList[self.Index])
        del self.InstructionList[self.Index]

    def AddTextToTerminal(self,text):
        for i in self.CurrentTerminals:
            i.AddTextToTerminal(text)

    def AddSceneEditor(self):

        def AddTerminal(ParnetEntity):
            TempTerminal = Terminal(self.AddTextToTerminal,parent = ParnetEntity)
            self.CurrentTerminals.append(TempTerminal)

            TempTerminal.Bg.scale_x = 1.35
            TempTerminal.Bg.origin = (.5,0,0)
            TempTerminal.UniversalParentEntity.origin = (.5,0,0)
            TempTerminal.UniversalParentEntity.position =  Vec3(0.887, -0.3, 2)
            TempTerminal.Bg.scale =  Vec3(1.35, 0.2, 1)
            TempTerminal.SetUp()


        self.CurrentProjectEditor.CurrentTabs.append(SceneEditor(enabled = True,SaveFunction= self.Save,AddTerminalFunc = Func(print,"hi"),ShowInstructionFunc = self.ShowInstruction,ExportToPyFunc=self.ExportProjectToPy,EditorDataDict=self.ConfiableEditorData,EditorCamera = self.EditorCamera))
        self.CurrentProjectEditor.CurrentTabs[-1].AddTerminal = Func(AddTerminal,self.CurrentProjectEditor.CurrentTabs[-1].UniversalParentEntity)

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
        self.CurrentProjectEditor.CurrentTabs.append(CodeEditorPython(ProjectName=self.CurrentProjectEditor.ProjectName,SaveFunction= self.Save,enabled=False,EditorDataDict=self.ConfiableEditorData,ignore = True,UdSrc=self.CurrentProjectEditor.UDSrc,OnFileAdded = self.CurrentProjectEditor.OnFileAdded,ShowInstructionFunc = self.ShowInstruction))

        self.CurrentProjectEditor.CurrentTabs[-1].name = f"Code Editor {len([i for i in range(len(self.CurrentProjectEditor.CurrentTabs)) if type(self.CurrentProjectEditor.CurrentTabs[i]).__name__ == 'CodeEditorPython'])}" 
        self.SetupEditor(self.CurrentProjectEditor.CurrentTabs[-1])
        self.CurrentProjectEditor.UpdateTabsMenu()

    def AddUrsaVisorEditor(self):
        self.CurrentProjectEditor.CurrentTabs.append(CodeEditorUrsaVisor(enabled=False,ignore = True,SaveFunction= self.Save,EditorDataDict=self.ConfiableEditorData))

        self.CurrentProjectEditor.CurrentTabs[-1].name = f"Ursa Editor {len([i for i in range(len(self.CurrentProjectEditor.CurrentTabs)) if type(self.CurrentProjectEditor.CurrentTabs[i]).__name__ == 'CodeEditorUrsaVisor'])}" 

        self.SetupEditor(self.CurrentProjectEditor.CurrentTabs[-1])
        self.CurrentProjectEditor.UpdateTabsMenu()


    def ConfigEditorAsSettings(self):
        self.StartingUi.ConfigEditorAsSettings(self.ConfiableEditorData)
        for i in range(len(self.ProjectEditorsList)):
            for j in range(len(self.ProjectEditorsList[i].CurrentTabs)):
                self.ProjectEditorsList[i].CurrentTabs[j].ConfigEditorAsSettings(self.ConfiableEditorData)

        self.MemoryCounter.enabled = self.ConfiableEditorData["Show memory counter"]
        self.StartingUi.EditorDataDict = self.ConfiableEditorData
        window.fullscreen = self.ConfiableEditorData["Fullscreen"]
        camera.clip_plane_near = self.ConfiableEditorData["Render distance (near)"]
        camera.clip_plane_far = self.ConfiableEditorData["Render distance (far)"]
        if self.ConfiableEditorData["Anti-aliasing sample"] > 0:
            self.Filter.delMSAA()
            self.Filter.setMSAA(self.ConfiableEditorData["Anti-aliasing sample"])
        else:
            self.Filter.delMSAA()

    def ExportProjectToPy(self,Path,ProjectName = None,InProjectEditor = True,Demo = False):
        if ProjectName is None:
            ProjectName = self.CurrentProjectEditor.ProjectName

        if Path != "":
            if InProjectEditor:
                self.Save()
            Path.replace("\\","/")
            Path += "/Exported games"
            # print(Path)

            ProjectExporter(ProjectName = ProjectName,ProjectPath=f'{self.FolderName}/Current Games',ToSavePath=Path,Demo = Demo)

            self.ShowInstruction("Exported successfully",KillAfter = 6,KillIn=3)
        else:
            self.ShowInstruction("Invalid path",KillAfter = 6,KillIn=3,Title = "Error")

    def PlayProject(self):
        self.CurrentProjectEditor.SaveProjectButton.on_click()
        self.ExportProjectToPy(CurrentFolderNameReturner(),self.CurrentProjectEditor.ProjectName,False,Demo = True)
        Sp = subprocess.Popen(["python", f"{CurrentFolderNameReturner()}/Exported games/{self.CurrentProjectEditor.ProjectName}/Main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._output, self._err = Sp.communicate()
        if Sp.returncode  != 0:
            self.ShowInstruction(f"The game encounterd an error\nOutput:{self._output} \nErr: {self._err}")

    def ReadyToHostProject(self):
        self.Port = 48513
        self.Ip = "localhost"

        self.Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


        return self.Port,self.Ip

    def HostProject(self,MaxJoin = 0):
        self.Server.bind((self.Ip,self.Port))
        if MaxJoin != 0:
            self.Server.listen(MaxJoin)
        else:
            self.Server.listen()

    def EnableWorldItemsAndSetProjectName(self,WorldItemsList,Project = ""):
        # self.StartingUi.StartProject()
        self.StartEdit()
        for item in WorldItemsList:
            # Evaluate the class constructor as an expression and append the result to the list
            self.CurrentProjectEditor.CurrentSceneEditor.WorldItems.append(eval(item['cls'] + item['args']))
        self.SetProjectName(Project)

    def SetProjectName(self,Value: str):
        self.CurrentProjectEditor.ProjectName = Value

    def RemoveProject(self,Name,Replace = False):
        if Replace is False:
            self.NonConfiableEditorData["CurrentProjectNames"].remove(Name)
            self.NonConfiableEditorData["RecentEdits"].remove(Name)

        else:
            if Replace not in self.NonConfiableEditorData["CurrentProjectNames"]:
                self.NonConfiableEditorData["CurrentProjectNames"][self.NonConfiableEditorData["CurrentProjectNames"].index(Name)] = Replace  
                self.NonConfiableEditorData["RecentEdits"][self.NonConfiableEditorData["RecentEdits"].index(Name)] = Replace  

        self.SaveData()

    def RegiveDataDict(self):
        return self.ConfiableEditorData,self.NonConfiableEditorData

    def RetakeDataDict(self,ConfigableEditorData,NonConfigableEditorData):
        self.ConfiableEditorData = ConfigableEditorData
        self.NonConfiableEditorData = NonConfigableEditorData

def BaseRunner():
    # import site

    # site_packages_path = site.getsitepackages()[0]

    app = Ursina()
    window.exit_button.disable()
    window.fps_counter.disable()
    application.development_mode = False
    window.cog_button.disable()

    Sky()

    Editor = UrsinaEditor(EditCam := EditorCamera()) # the ':=' operator is called walrus operator. google it!  
    Editor.Setup()
    app.run()

if __name__ == "__main__":
    BaseRunner()    
