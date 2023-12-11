from GamePlusEditor.ursina import *
from GamePlusEditor.OtherStuff import CustomWindow,ReplaceValue,PrepareForRecentProjects,CurrentFolderNameReturner,OpenBrowser,MultiFunctionCaller,BoolInverter,RecursivePerformer,DeleteProject
from GamePlusEditor.ursina.prefabs.dropdown_menu import DropdownMenuButton
from GamePlusEditor.ursina.prefabs.dropdown_menu import SimpleDropdownMenu
from GamePlusEditor.RecentProjectFinder import GetRecentProjects
from GamePlusEditor.ProjectLoader import LoadProjectToScene
from GamePlusEditor.CoreFiles.TrueFalseIndicator import TrueFalseIndicator
from GamePlusEditor.CoreFiles.ConfigProjectMenu import ConfigProjectManager
from GamePlusEditor.OpenFile import Openselector
from GamePlusEditor.Netwroking.JoinProjectMenu import JoinProjectMenu

class StartingUI(Entity):
    def __init__(self,EditorDataDictConfigable,EditorDataDictNonConfigable,RegiveDataDictFunc,RetakeDataDictFunc,OnProjectStart,ProjectName,SaveNonConfiableData,ShowInstructionFunc,ChangeConfigDataToDefaultTypeFunc,FuncToEnableOnOpen,ExportToPyFunc,RemoveProjectNameFunc,ProjectSettings={"ProjectGraphicsQuality": "Low","ProjectLanguage": "Python","ProjectNetworkingOnline": False,"CurrentTargatedPlatform": "windows","CurrentProjectBase": "FPC"},OpenedProjects = []):
        super().__init__(parent = camera.ui)

        self.ProjectName = ProjectName
        self.ProjectSettings = ProjectSettings
        self.EditorDataDictConfigable = EditorDataDictConfigable
        self.OnProjectStart = OnProjectStart
        self.ShowInstructionFunc = ShowInstructionFunc
        self.SaveNonConfiableData = SaveNonConfiableData
        self.FuncToEnableOnOpen = FuncToEnableOnOpen
        self.HasRecentProjectShow = False
        self.ExportToPyFunc = ExportToPyFunc
        self.RemoveProjectNameFunc = RemoveProjectNameFunc
        self.RetakeDataDict = RetakeDataDictFunc
        self.RegiveDataDictFunc = RegiveDataDictFunc
        # self.OrderOfRecentProjects: list = RecentProjectsOrder
        self.EditorDataDictNonConfigable = EditorDataDictNonConfigable
        self.ProjectDataName = ["ProjectGraphicsQuality","ProjectLanguage","ProjectNetworkingOnline","CurrentTargatedPlatform","CurrentProjectBase"]
        self.RecentProjectButtonTexts = ("Open project","Config project","Finish project","Delete project")
        self.OtherOptionsText = ["Official site","View on github","Watch youtube tutorial","Load an exported project","View plugins","Join project"]
        self.OtherOptionsFunc = [Func(print_on_screen,"Site not done yet!",position = (0,.1),color = color.blue,duration =2),Func(OpenBrowser,"https://github.com/IndividualCoder/UrsinaEditor"),Func(print_on_screen,"No tutorials yet (•_•)",position = (0,.1),color = color.blue,duration =2),Func(print_on_screen,"Even the logic is not built yet :/",position = (0,.1),color = color.blue,duration =2),Func(print_on_screen,"No plugins yet!",position = (0,.1),color = color.blue,duration =2),Func(JoinProjectMenu,self.EnableStaringUI,self.DisableStartingUI)]


        self.ChangeConfigDataToDefaultTypeFunc = ChangeConfigDataToDefaultTypeFunc
        self.OpenedProjects = OpenedProjects


        self.UniversalParentEntity = Entity(parent = self)
        self.StartingUIParentEntity = Entity(parent = self.UniversalParentEntity)
        self.RecentProjectsParentEntity = Entity(parent = self.StartingUIParentEntity)
        self.RecentProjectsScrollerParentEntity = Button(name  = "RecentProjectEntity",parent = self.RecentProjectsParentEntity,scale = Vec3(1.77792, 0.535418, 1),position = Vec3(-0.889999, -0.232639, 1),color = color.white,visible_self = False,radius=0,origin = (-.5,0,0))
        self.CreateNewProjectMenuParentEntity = Entity(parent = self.UniversalParentEntity,enabled = False)
        self.ChangeVarsMenuParentEntity = Entity(parent = self.UniversalParentEntity,enabled = False)
        self.ChangeVarsTextParentEntity = Entity(parent = self.ChangeVarsMenuParentEntity)

        self.ConfigProjectManager = ConfigProjectManager(Parent=self.UniversalParentEntity,Path=f"{CurrentFolderNameReturner()}/Current Games",CancelClick=Func(MultiFunctionCaller,self.EnableStaringUI,self.ShowRecentProjects),ToSaveDataFunc = self.RenameProject)

        self.RecentProjectsScrollEntity = None

        self.CreateNewProjectButton = Button(parent = self.StartingUIParentEntity,text="Create new project",radius=.2,Key="1", on_key_press = self.ShowCreateNewProject,on_click = self.ShowCreateNewProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.384259, 0))
        self.ChangeVarsButton = Button(parent = self.StartingUIParentEntity,text="Change vars",radius=.2,Key="2", on_key_press = self.ChangeVarsMenu,on_click = self.ChangeVarsMenu,scale = (0.4,0.2),position = Vec3(0.56713, 0.384259, 0))
        self.OtherOptionsButton = Button(parent = self.StartingUIParentEntity,text="More options",radius=.2,Key="3",on_click = self.ShowOtherOptionsFunc,scale = (0.4,0.2),position = Vec3(-0.56713, 0.163194, 0))
        self.QuitApplicationButton = Button(parent = self.StartingUIParentEntity,text="Close editor",radius=.2,Key=["escape",'4'], on_key_press = self.CheckUserQuit,on_click = self.CheckUserQuit,scale = (0.4,0.2),position = Vec3(0.56713, 0.163194, 0))

        self.BackgroundOfRecentProjects = Entity(parent = self.RecentProjectsParentEntity,model = "cube",color = color.gray,scale = Vec3(1.77792, 0.535418, 0),position = Vec3(0, -0.232639, 0))

        self.LineOnTop = Entity(name = "LineOnTop",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = 5,position = Vec3(0, 0.405, -10),color = color.gray,z = -10)
        self.LineBetweenTypeAndInputFieldLine = Entity(name = "LineBetweenTypeAndInputFieldLine",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = len(list(self.EditorDataDictConfigable)),rotation_z = 90,position = Vec3(0.03, 0, -10),color = color.gray,z = -10)
        self.LineBetweenInputFieldAndDescriptionLine = Entity(name = "LineBetweenInputFieldAndDescriptionLine",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = len(list(self.EditorDataDictConfigable)),rotation_z = 90,position = Vec3(0.375, 0, -10),color = color.gray,z = -10)
        self.GoBackOfChangeVarsMenuButton = Button(name = "Go Back Of Change Vars Menu Button",parent = self.ChangeVarsMenuParentEntity,text="Done",Key="escape",on_click = Sequence(Func(self.DestroyChangeVarsMenuButtons),Func(self.ChangeVarsMenuParentEntity.disable),Func(self.EnableStaringUI)),radius=0,scale = Vec3(0.280001, 0.0800007, 1),position = Vec3(-0.744999, 0.455, 0))
        self.LineBetweenNameAndTypeLine = Entity(name = "LineBetweenNameAndTypeLine",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = len(list(self.EditorDataDictConfigable)),rotation_z = 90,position = (-.38,0),color = color.gray,z = -10)
        self.BackgroundOfChangeVarsMenu = Entity(parent = self.ChangeVarsMenuParentEntity,model = "cube",color = color.rgba(0,0,0,200),scale = Vec3(10,10, 0),position = Vec3(0, 0, 0))
        self.SaveChangedVarsButton = Button(parent = self.ChangeVarsMenuParentEntity,text="Save",radius=0,hover_highlight=True,hover_highlight_size=1,highlight_color = color.light_blue,model = "cube",color = color.light_blue,scale = Vec3(0.22, 0.14, 1),position = Vec3(-0.02, -0.34, -20),on_click = self.SaveNonConfiableData,Key = "s",partKey="control")

        self.CreateNewProjectFpcButton = Button(name = "FPC",parent = self.CreateNewProjectMenuParentEntity,text="FPC\nFirst person controller",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (-0.68, 0.3, 0),on_click = Func(self.CreateNewProject,"FPC"),Key = "1",on_key_press=Func(self.CreateNewProject,"FPC"),color = color.tint(color.green,-.5)) #Game is based on First person controller (3d)
        self.CreateNewProjectTpcButton = Button(name = "TPC",parent = self.CreateNewProjectMenuParentEntity,text="TPC\nThird person controller",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (-0.37, 0.3, 0),on_click = Func(self.CreateNewProject,"TPC"),Key = "2",on_key_press=Func(self.CreateNewProject,"TPC")) #Game is based on Third person controller (3d)
        self.CreateNewProjectTopDownButton = Button(name = "Top down",parent = self.CreateNewProjectMenuParentEntity,text="Top-Down\nTop-down game (3d)",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (-0.06, 0.3, 0),on_click = Func(self.CreateNewProject,"TopDown"),Key = "3",on_key_press=Func(self.CreateNewProject,"TopDown")) #Game is based on Top-Down made (2d)
        self.CreateNewProjectPlatformerButton = Button(name = "2d",parent = self.CreateNewProjectMenuParentEntity,text="Platformer\n2d platformer",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (0.25, 0.3, 0),on_click = Func(self.CreateNewProject,"Platformer"),Key = "4",on_key_press=Func(self.CreateNewProject,"Platformer")) #Game is based on  platformer mode (2d)
        self.CreateNewProjectFpcAndTpcButton = Button(name = "FPC/TPC",parent = self.CreateNewProjectMenuParentEntity,text="FPC/TPC\nBoth Fpc and Tpc",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (0.56, 0.3, 0),on_click = Func(self.CreateNewProject,"FPCTPC"),Key = "5",on_key_press=Func(self.CreateNewProject,"FPCTPC")) #Game is based on both FPC and TPC
        self.CreateNewProjectBaseDict = {"FPC": self.CreateNewProjectFpcButton,"TPC": self.CreateNewProjectTpcButton,"TopDown": self.CreateNewProjectTopDownButton,"Platformer": self.CreateNewProjectPlatformerButton,"FPCTPC": self.CreateNewProjectFpcAndTpcButton} # Made a dict to avoid multiple if
        self.CurrentProjectBase = self.CreateNewProjectBaseDict["FPC"]

        self.ProjectTitleButton = InputField(name = "Title input field",parent = self.CreateNewProjectMenuParentEntity,placeholder="Enter your project's title",enabled = False,active = False,position = (-.485,.15),origin_x = 0,radius = 0,scale = (.66,.05),submit_on="enter",limit_content_to = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
        self.LanguageText = Text(name = "Select project language text",parent = self.CreateNewProjectMenuParentEntity,text="Language",position = (-0.8, 0.105, 0),scale = 1) #-0.81, 0.09, 0
        self.LanguageText.create_background(.03,0)
        self.LanguageMenuParentEntity = Entity(name = "Language parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = (.3,.2),enabled = False,position = (-0.664, -.040,1))
        self.LanguagePythonButton = Button(parent = self.LanguageMenuParentEntity,text = "Python",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (.7,.3),enabled = False,position = (.15,-.214,-1),radius = 0,on_click = self.SetProjectLanguage)
        self.LanguageUrsaVisorButton = Button(parent = self.LanguageMenuParentEntity,text = "Ursa-visor",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (.7,.3),enabled = False,position = (-.15,.214,-1),radius = 0,on_click = self.SetProjectLanguage)

        self.TargatedPlatformText = Text(name = "Select project targated platform text",parent = self.CreateNewProjectMenuParentEntity,text="Targated platform",position = (-0.485, 0.105, 0),scale = 1)
        self.TargatedPlatformText.create_background(.03,0)
        self.TargatedPlatformDropdownMenu =     SimpleDropdownMenu(name = "Dropdown menu",parent = self.CreateNewProjectMenuParentEntity,text = 'Windows',color = color.black66,highlight_color = color.blue.tint(.2),on_click = Func(self.SetProjectTargatedPlatform,"windows"), buttons=(DropdownMenuButton(name = 'Android',text="Android",color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"android")),DropdownMenuButton('Mac',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"mac")),DropdownMenuButton('ios',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"ios")),DropdownMenuButton('Linux',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"linux"))),click_to_open=True,position = (-.5,0.06),scale = (.25,0.025))
        self.TargatedPlatformBaseDict = {"windows": self.TargatedPlatformDropdownMenu,"android": self.TargatedPlatformDropdownMenu.buttons[0],"mac": self.TargatedPlatformDropdownMenu.buttons[1],"ios": self.TargatedPlatformDropdownMenu.buttons[2],"linux": self.TargatedPlatformDropdownMenu.buttons[3]}
        self.CurrentTargatedPlatform = self.TargatedPlatformBaseDict["windows"]

        self.ProjectNetworkingText = Text(name = "Select project networking text",parent = self.CreateNewProjectMenuParentEntity,text="Networking",position = (-0.8, -0.1649999, 0),scale = 1)
        self.ProjectNetworkingText.create_background(.03,0)
        self.ProjectNetworkingMenuParentEntity = Entity(name = "Networking parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = (.3,.2),enabled = False,position = (-0.664, -.31,60))
        self.ProjectNetworkignOnlineButton = Button(parent = self.ProjectNetworkingMenuParentEntity,text = "Offline",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (1,.3),enabled = False,position = (0,-.214,-20),radius = 0,on_click = self.SetProjectNetworking)
        self.ProjectNetworkignOfflineButton = Button(parent = self.ProjectNetworkingMenuParentEntity,text = "Online",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (1,.3),enabled = False,position = (0,.214,-20),radius = 0,on_click = self.SetProjectNetworking)

        self.ProjectGraphicsQualityText = Text(name = "Select project graphics quality text",parent = self.CreateNewProjectMenuParentEntity,text="Select graphics quality",position = (-0.49, -0.1, 0),scale = 1)
        self.ProjectGraphicsQualityText.create_background(.03,0)
        self.ProjectGraphicsQualityMenuParentEntity = Entity(name = "Graphics parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = Vec3(0.3, 0.26, 1),enabled = False,position = (-0.354, -0.28, 60))

        self.ProjectGraphicsQualityLowButton = Button(name = "Low",parent = self.ProjectGraphicsQualityMenuParentEntity,text = "Low",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (1,.25),enabled = False,position = (0,.336667,-20),radius = 0,on_click = Func(self.SetProjectGraphicsQuality,"Low"))
        self.ProjectGraphicsQualityMediumButton = Button(name = "Medium",parent = self.ProjectGraphicsQualityMenuParentEntity,text = "Medium",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (1,.25),enabled = False,position = (0,.0033333,-20),radius = 0,on_click = Func(self.SetProjectGraphicsQuality,"Medium"))
        self.ProjectGraphicsQualityHighButton = Button(name = "High",parent = self.ProjectGraphicsQualityMenuParentEntity,text = "High (AAA)",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (1,.25),enabled = False,position = (0,-.33,-20),radius = 0,on_click = Func(self.SetProjectGraphicsQuality,"High"))
        self.CurrentGraphicsQuality = self.ProjectGraphicsQualityMediumButton
        self.StartProjectButton = Button(name = "Start button of create new project menu",parent = self.CreateNewProjectMenuParentEntity,text="Start",Key = "enter",scale = (.3,.25),on_click = Func(invoke,self.StartProject,delay = .1))

    def ShowCreateNewProject(self):
        self.DisableStartingUI()
        self.EnableCreateNewProjectMenuButtons()
        self.EnableLanguageButtons()
        self.EnableNetworkingButtons()
        self.EnableGraphicsQualityButtons()
        invoke(self.ProjectTitleButton.MakeActive,delay = .1)

    def RenameProject(self,Name,Replace = False):
        if Replace is False:
            self.RemoveProjectNameFunc(Name)
            return
        self.RemoveProjectNameFunc(Name,Replace)
        self.EditorDataDictConfigable,self.EditorDataDictNonConfigable = self.RetakeDataDict()

    def CreateNewProject(self,NewProjectBase):
        if not self.ProjectTitleButton.active:
            ReplaceValue(self.CurrentProjectBase,self.CreateNewProjectBaseDict[NewProjectBase])
            ReplaceValue(self.CurrentProjectBase,self.CreateNewProjectBaseDict[NewProjectBase],"highlight_color")
            # print_on_screen(NewProjectBase,origin=(0,0,0),color=color.black,duration=1)
            # self.CreateNewProjectFpcButton.color = color.blue.tint(-.4)
            self.CurrentProjectBase = self.CreateNewProjectBaseDict[NewProjectBase]
            # print(self.CurrentProjectBase)
            self.ProjectSettings["CurrentProjectBase"] = self.CreateNewProjectBaseDict[NewProjectBase].name

    def SetProjectName(self):
        # print("func setProjectName from starting ui is running")
        # print(self.ProjectTitleButton.text)
        self.ProjectName = self.ProjectTitleButton.text
        self.ProjectTitleButton.active = False
        self.ProjectTitleButton.text = ""

    def SetProjectLanguage(self):
        ReplaceValue(self.LanguagePythonButton,self.LanguageUrsaVisorButton)
        ReplaceValue(self.LanguagePythonButton,self.LanguageUrsaVisorButton,"highlight_color")

        if self.ProjectSettings["ProjectLanguage"] == "Ursa-visor":
            self.ProjectSettings["ProjectLanguage"] = "Python"
        else:
            self.ProjectSettings["ProjectLanguage"] = "Ursa-visor"

        # print(self.ProjectLanguage)

    def SetProjectTargatedPlatform(self,New):
        try:
            ReplaceValue(self.TargatedPlatformBaseDict[New],self.CurrentTargatedPlatform,"text")
            ReplaceValue(self.TargatedPlatformBaseDict[New],self.CurrentTargatedPlatform,"text_entity")
            # ReplaceValue(self.TargatedPlatformBaseDict[New],self.CurrentTargatedPlatform,"on_click")
            self.ProjectSettings["CurrentTargatedPlatform"] = New

        except:
            print_on_screen("An error occured. Terminating function")

    def SetProjectNetworking(self):
        ReplaceValue(self.ProjectNetworkignOfflineButton,self.ProjectNetworkignOnlineButton)
        ReplaceValue(self.ProjectNetworkignOfflineButton,self.ProjectNetworkignOnlineButton,"highlight_color")

        self.ProjectSettings["ProjectNetworkingOnline"] = not self.ProjectSettings["ProjectNetworkingOnline"]

    def SetProjectGraphicsQuality(self,New):
        if New == "Low":
            ReplaceValue(self.CurrentGraphicsQuality,self.ProjectGraphicsQualityLowButton)
            ReplaceValue(self.CurrentGraphicsQuality,self.ProjectGraphicsQualityLowButton,"highlight_color")
            self.CurrentGraphicsQuality = self.ProjectGraphicsQualityLowButton
        elif New == "Medium":
            ReplaceValue(self.CurrentGraphicsQuality,self.ProjectGraphicsQualityMediumButton)
            ReplaceValue(self.CurrentGraphicsQuality,self.ProjectGraphicsQualityMediumButton,"highlight_color")
            self.CurrentGraphicsQuality = self.ProjectGraphicsQualityMediumButton
        elif New == "High":
            ReplaceValue(self.CurrentGraphicsQuality,self.ProjectGraphicsQualityHighButton)
            ReplaceValue(self.CurrentGraphicsQuality,self.ProjectGraphicsQualityHighButton,"highlight_color")
            self.CurrentGraphicsQuality = self.ProjectGraphicsQualityHighButton

        self.ProjectSettings["ProjectGraphicsQuality"] = New
        # print(["self.ProjectGraphicsQuality"])

    def StartProject(self):
        if not self.ProjectTitleButton.active:
            self.ProjectTitleButton.text = self.ProjectTitleButton.text.replace(" ","-")
            if self.ProjectTitleButton.text.replace(" ","") == "":
                # print_on_screen("Enter your project's name.",color = color.red,origin = (0,0),duration=3,position = (.5,-.1),scale = 1.2)
                self.ShowInstructionFunc("Enter your project's name!\nIt is compulsory.",Title = 'No name?',WordWrap = 50)
                return

            elif self.ProjectTitleButton.text in self.EditorDataDictNonConfigable["CurrentProjectNames"]:
                    # print_on_screen("You already have a project with this name.\nChoose a new one",color = color.red,origin = (0,0),duration=3,position = (.5,-.1),scale = 1.2)
                self.ShowInstructionFunc("You already have a project with this name.\nChoose a new one",Title = "Error")
                return

            self.CreateNewProjectMenuParentEntity.disable()
            self.EditorDataDictNonConfigable["RecentEdits"].insert(0,self.ProjectTitleButton.text)
            self.SetProjectName()
            self.OnProjectStart()

    def ChangeVarsMenu(self):
        self.ChangeVarsTextParentEntity.enable()
        self.DisableStartingUI()
        for i in range(len(list(self.EditorDataDictConfigable))*2):
            if i % 2 == 0:
                self.ChangeVarsTextParentEntity.children.append(Text(name = f"Change var children_{i}",text=list(self.EditorDataDictConfigable)[int(i/2)],parent  = self.ChangeVarsTextParentEntity,position = (-.87,.39-i/2*0.07,-10),scale = 1.75)) 
            else:
                self.ChangeVarsTextParentEntity.children.append(Entity(name = f"Line_{i}",parent = self.ChangeVarsTextParentEntity,model = "line",scale = 2,position = (0,.37-i/2*0.07),color = color.gray,z = -10)) 
 
        # self.TypeVarList = [type(sublist).__name__ for sublist in self.EditorDataDict.values()]

        for i in range(len([type(sublist).__name__ for sublist in self.EditorDataDictConfigable.values()])):
            self.ChangeVarsTextParentEntity.children.append(Text(name = f"change var type {i}",parent=self.ChangeVarsTextParentEntity,text=([type(sublist).__name__ for sublist in self.EditorDataDictConfigable.values()][i]),position = Vec3(-0.37, 0.39-i*0.07, -10),scale = 1.75))

        # self.ValueVarList = [sublist for sublist in self.EditorDataDict.values()]
  
        for i in range(len([sublist for sublist in self.EditorDataDictConfigable.values()])):
            if str([sublist for sublist in self.EditorDataDictConfigable.values()][i]) in ("True","False"):
                self.ChangeVarsTextParentEntity.children.append(TrueFalseIndicator(["True","False"],OnClick=self.OnEditorVarsChanged,position = Vec3(0.2, 0.37-i*0.07, -10),scale = Vec3(0.32, 0.05, 1),parent = self.ChangeVarsTextParentEntity,name = i,DefaultState=str([sublist for sublist in self.EditorDataDictConfigable.values()][i])))
            elif type([sublist for sublist in self.EditorDataDictConfigable.values()][i]).__name__ in ("int","float"):
                self.ChangeVarsTextParentEntity.children.append(InputField(name = i,parent = self.ChangeVarsTextParentEntity,character_limit = 16,default_value=str([sublist for sublist in self.EditorDataDictConfigable.values()][i]),position = Vec3(0.2, 0.37-i*0.07, -10),scale = Vec3(0.32, 0.05, 1),active = False,escape_active=True,submit_on="enter",on_submit = Func(self.OnEditorVarsChanged),limit_content_to = "1234567890."))

        self.EnableChangeVarsMenuButtons()

    def OnEditorVarsChanged(self):
        # for i in range(len(list(self.EditorDataDict))):
        self.DataToPut = []
        for i in range(len(self.ChangeVarsTextParentEntity.children)):
            if type(self.ChangeVarsTextParentEntity.children[i]).__name__ == "InputField":
                self.DataToPut.append(self.ChangeVarsTextParentEntity.children[i].text)
                self.ChangeVarsTextParentEntity.children[i].active  = False
            elif type(self.ChangeVarsTextParentEntity.children[i]).__name__ == "TrueFalseIndicator":
                self.DataToPut.append(self.ChangeVarsTextParentEntity.children[i].Button.text)
                # print(self.ChangeVarsTextParentEntity.children[i].Button.text)

        self.EditorDataDictConfigable = dict(zip(list(self.EditorDataDictConfigable),self.DataToPut))
        # print(f"{__file__} :: {self.EditorDataDict}")

        self.ChangeConfigDataToDefaultTypeFunc(self.EditorDataDictConfigable)


    def DestroyChangeVarsMenuButtons(self):
        self.TempVar = len(self.ChangeVarsTextParentEntity.children)
        # print(self.TempVar)
        for i in range(self.TempVar - 1, -1, -1):
            # del self.ChangeVarsTextParentEntity.children[i]
            destroy(self.ChangeVarsTextParentEntity.children[i])

        del self.TempVar


    def ShowOtherOptionsFunc(self):
        # print(len(self.OtherOptionsButton.children))
        if len(self.OtherOptionsButton.children) ==1:
            self.TempButtonListDict = {}
            self.OtherOptionsButton.children.append(ButtonList(self.TempButtonListDict,button_height = 1.4,parent = self.OtherOptionsButton,render_queue = 2,z = -100,scale_x = 2,scale_y = 4,always_on_top = True))
            self.TempButtonListDict = {self.OtherOptionsText[i]: Func(MultiFunctionCaller,self.OtherOptionsButton.children[-1].disable,self.OtherOptionsFunc[i]) for i in range(len(self.OtherOptionsText))}

            self.OtherOptionsButton.children[-1].button_dict = self.TempButtonListDict
            self.OtherOptionsButton.children[-1].bg.color = color.black
            self.OtherOptionsButton.children[-1].text_entity.render_queue = 2
            self.OtherOptionsButton.children[-1].highlight.color = color.azure

            self.OtherOptionsButton.children[-1].bg_button = Button(parent = self.OtherOptionsButton.children[-1],render_queue = 1,scale = 100,on_click = self.OtherOptionsButton.children[-1].disable,z = 10,highlight_color = color.black50,pressed_color = color.black50,color = color.black50,Key = "escape")

        else:
            self.OtherOptionsButton.children[-1].enable()

    def CheckUserQuit(self,ToCheck = "Quit?"):
        if ToCheck == "Quit?":
            if len(self.OtherOptionsButton.children) == 1 or not self.OtherOptionsButton.children[1].enabled:
                invoke(CustomWindow,ToEnable=self.EnableEverything,OnEnable=self.DisableEverything,title = "Quit?",B1Key=["1" ,"escape"],B2Key=["2","enter"],delay = .1)
        else:
            invoke(CustomWindow,ToEnable=self.EnableEverything,OnEnable=self.DisableEverything,text = "Are you sure you want to delete this project",ToEnableOnYes = Func(MultiFunctionCaller,Func(DeleteProject,ToCheck,f"{CurrentFolderNameReturner()}/Current Games"),Func(self.RemoveProjectNameFunc,ToCheck),self.EnableEverything,self.ShowRecentProjects),title = "Sure?",B1Key=["1" ,"escape"],B2Key=["2","enter"],delay = .1)


    def ShowRecentProjects(self,FuncToEnableOnOpen = None):
        if FuncToEnableOnOpen is None:
            FuncToEnableOnOpen = self.FuncToEnableOnOpen

        if self.HasRecentProjectShow is True:
            self.RecentProjectsScrollerParentEntity.scale = Vec3(1.77792, 0.535418, 1)
            RecursivePerformer(self.RecentProjectsScrollerParentEntity.children,destroy,BasicFunc=False)
            for i in range(len(self.RecentProjectsScrollerParentEntity.scripts)): self.RecentProjectsScrollerParentEntity.scripts.remove(self.RecentProjectsScrollerParentEntity.scripts[i])
            self.RecentProjectsScrollerParentEntity.scripts = []
            # self.HasRecentProjectShow = False

        self.RecentProjectsText = Text(name = "RecentProjectsText",parent = self.RecentProjectsParentEntity,text = "Recent projects",position = Vec3(-0.879999, 0.025, 0),scale = 1.5)
        self.RecentProjectsLine = Entity(name = "RecentProjectsLine",parent = self.RecentProjectsParentEntity,model = "line",position = Vec3(0, -0.02, 0),scale = Vec3(1.78, 0.85, 1))
        self.TotalRunningProjects = self.LoadRecentProjects()
        # print("....",self.TotalRunningProjects)
        if self.TotalRunningProjects == {}:
            invoke(self.ShowInstructionFunc,"Looks like you are new to this editor. You should first watch tutorial to get a working understanding of the editor",KillAfter = 7,delay = .8)

        self.SetRecentProjects(ProjectSettings=self.TotalRunningProjects,FuncToEnableOnOpen=FuncToEnableOnOpen)

    def LoadRecentProjects(self,ReturnOrder = None):
        CurrentFolderName = CurrentFolderNameReturner()
        # print("mine",CurrentFolderName)
        CurrentFolderName = CurrentFolderName.replace("\\","/")
        CurrentFolderName = CurrentFolderName + "/Current Games"

        # print(CurrentFolderName)
        return GetRecentProjects(CurrentFolderName,order=ReturnOrder)

    def SetRecentProjects(self,ProjectSettings: dict,FuncToEnableOnOpen):

        self.NewData = dict(sorted(ProjectSettings.items(), key=lambda item: self.EditorDataDictNonConfigable["RecentEdits"].index(item[0])))

        for i,j in enumerate(self.NewData):
            self.TopParent = Button(parent = self.RecentProjectsScrollerParentEntity,radius=  0,position = Vec3(0-i*-0.3, 0, 0),scale_x = .3,origin = (-.5,0,0),visible_self = False)
            Text(parent = self.TopParent,text=j,position = Vec3(.05, 0.366999, 0),scale = Vec3(3, 2.39, 1),always_on_top = True)
            Entity(parent = self.TopParent,model = "line",position = Vec3(1, -0.0529997, 0),scale = Vec3(0.899999, 0.2, 0.1),rotation_z = 90,always_on_top = True)
            self.ConfigProjectManager.CurrentProjectName = j

            Button(parent = self.TopParent,radius=.15,text= self.RecentProjectButtonTexts[0],color = color.blue,scale = Vec3(0.4,.16,1),position = (.25,-.2,-1),always_on_top = True,on_click = Func(self.OpenProject,FileName = j,FilePath = f"{CurrentFolderNameReturner()}/Current Games",FuncToEnableOnOpen = FuncToEnableOnOpen,ProjectName = j))
            Button(parent = self.TopParent,radius=.15,text= self.RecentProjectButtonTexts[1],color = color.blue,scale = Vec3(0.4,.16,1),position = (.75,-.2,-1),always_on_top = True,on_click = Func(MultiFunctionCaller,self.StartingUIParentEntity.disable,Func(RecursivePerformer,self.ConfigProjectManager.UniversalParentEntity),Func(self.ConfigProjectManager.Show,j)))
            Button(parent = self.TopParent,radius=.15,text= self.RecentProjectButtonTexts[2],color = color.blue,scale = Vec3(0.4,.16,1),position = (.25,-.4,-1),always_on_top = True,on_click = Func(self.ExportProject,j))
            Button(parent = self.TopParent,radius=.15,text= self.RecentProjectButtonTexts[3],color = color.blue,scale = Vec3(0.4,.16,1),position = (.75,-.4,-1),always_on_top = True,on_click = Func(self.CheckUserQuit,j))
            currentPro = self.NewData[j]
            for k,l in enumerate(self.ProjectDataName):
                Text(parent = self.TopParent,text=f"{PrepareForRecentProjects(self.ProjectDataName[k])}: {currentPro[l]}",position = Vec3(.1, 0.27-k*.07, 0),scale = Vec3(2, 2.19, 1),always_on_top = True)



        self.LineTemp = Entity(parent = self.RecentProjectsScrollerParentEntity,model = "line",position = Vec3(0, 0.298, 0),scale_x = len(self.NewData)*2)
        self.GetRecentProjectsScroll(len(self.NewData))
        self.LineTemp.scale_x = len(self.NewData)*2
        del self.LineTemp
        self.HasRecentProjectShow = True

    def GetRecentProjectsScroll(self,Len):
        if Len > 3:
            self.RecentProjectsScrollEntity = self.RecentProjectsScrollerParentEntity.add_script(Scrollable(max = -.9,min = -1.25,axis = 'x',scroll_speed = .01))

            self.RecentProjectsScrollerParentEntity.scale_x += .354
            for i in range(len(self.RecentProjectsScrollerParentEntity.children)):
                    self.RecentProjectsScrollerParentEntity.children[i].scale_x = .533 / self.RecentProjectsScrollerParentEntity.scale_x

            for i in range(1,len(self.RecentProjectsScrollerParentEntity.children)):
                # self.RecentProjectsScrollerParentEntity.children[i].x = self.RecentProjectsScrollerParentEntity.children[i-1].x + .01
                self.RecentProjectsScrollerParentEntity.children[i].x = self.RecentProjectsScrollerParentEntity.children[i-1].x + (self.RecentProjectsScrollerParentEntity.children[i].scale_x) * 1

            if Len > 4:
                Len -= 4
                for i in range(Len):
                    self.RecentProjectsScrollerParentEntity.scale_x += .533
                    self.RecentProjectsScrollEntity.update_target("min",self.RecentProjectsScrollEntity.min + -.5265)

                    for i in range(len(self.RecentProjectsScrollerParentEntity.children)):
                            self.RecentProjectsScrollerParentEntity.children[i].scale_x = .533 / self.RecentProjectsScrollerParentEntity.scale_x

                    for i in range(1,len(self.RecentProjectsScrollerParentEntity.children)):
                        # self.RecentProjectsScrollerParentEntity.children[i].x = self.RecentProjectsScrollerParentEntity.children[i-1].x + .01
                        self.RecentProjectsScrollerParentEntity.children[i].x = self.RecentProjectsScrollerParentEntity.children[i-1].x + (self.RecentProjectsScrollerParentEntity.children[i].scale_x) * 1

            # for i in range(1,len(self.RecentProjectsScrollerParentEntity.children)):
            #     if type(self.RecentProjectsScrollerParentEntity.children[i]).__name__ == "Button":
            #         if self.RecentProjectsScrollerParentEntity.children[i].text_entity is not None:
            #             self.RecentProjectsScrollerParentEntity.children[i].text =self.RecentProjectsScrollerParentEntity.children[i].text
            #             self.RecentProjectsScrollerParentEntity.children[i].text_entity.scale = 1


    def ExportProject(self,Name):
        self.ExportToPyFunc(Openselector(title="Choose folder"),Name,False)

    def DisableEverything(self):
        self.UniversalParentEntity.disable()

    def DisableStartingUI(self):
        self.StartingUIParentEntity.disable()


    def EnableEverything(self):
        self.UniversalParentEntity.enable()
        for i in range(len(self.StartingUIParentEntity.children)):
            self.StartingUIParentEntity.children[i].enable()

    def EnableStaringUI(self):
        self.StartingUIParentEntity.enable()
        for i in range(len(self.StartingUIParentEntity.children)):
            self.StartingUIParentEntity.children[i].enable()

    def EnableChangeVarsMenuButtons(self):
        self.ChangeVarsMenuParentEntity.enable()
        for i in range(len(self.ChangeVarsMenuParentEntity.children)):
            self.ChangeVarsMenuParentEntity.children[i].enable()

    def EnableCreateNewProjectMenuButtons(self):
        self.CreateNewProjectMenuParentEntity.enable()
        for i in range(len(self.CreateNewProjectMenuParentEntity.children)):
            self.CreateNewProjectMenuParentEntity.children[i].enable()

    def EnableLanguageButtons(self):
        for i in range(len(self.LanguageMenuParentEntity.children)):
            self.LanguageMenuParentEntity.children[i].enable()

    def EnableNetworkingButtons(self):
        for i in range(len(self.ProjectNetworkingMenuParentEntity.children)):
            self.ProjectNetworkingMenuParentEntity.children[i].enable()

    def EnableGraphicsQualityButtons(self):
        for i in range(len(self.ProjectGraphicsQualityMenuParentEntity.children)):
            self.ProjectGraphicsQualityMenuParentEntity.children[i].enable()


    def Setup(self):
        self.SetProjectGraphicsQuality("Medium")
        if self.OpenedProjects == []:
            # self.SaveChangedVarsButton._on_click = self.SaveData
            self.SaveChangedVarsButton.text_entity.color = color.black
            self.SaveChangedVarsButton.text_entity.always_on_top = True
            self.SaveChangedVarsButton.highlight_button.scale_x -= 0.1
            # self.SaveChangedVarsButton.highlight_button.z = 10
            # self.SaveChangedVarsButton.z  = -20
            self.ConfigEditorAsSettings(self.EditorDataDictConfigable)

    def ConfigEditorAsSettings(self,DataDict):
        self.SetTooltip(DataDict["Show tooltip"])

    def SetTooltip(self,value):
        self.ItemToToolTipList = [self.CreateNewProjectFpcButton,self.CreateNewProjectTpcButton,self.CreateNewProjectTopDownButton,self.CreateNewProjectPlatformerButton,self.CreateNewProjectFpcAndTpcButton,self.LanguagePythonButton,self.LanguageUrsaVisorButton,self.ProjectNetworkignOnlineButton,self.ProjectNetworkignOfflineButton,self.ProjectGraphicsQualityLowButton,self.ProjectGraphicsQualityMediumButton,self.ProjectGraphicsQualityHighButton,self.SaveChangedVarsButton]
        if value:
            self.ToolTipList = ["First person games like valorant, cod etc","Third person games like pubg, gta etc","Camera is stuck at one place but not in 2d, this category is also called '2.5d games',like clash of clans, clash royale etc","2d game where camera is stuck at one place in 2d","Both TPC and FPC","If enabled,the little amount to code you will have to write will be in python","If enabled,the little amount to code you will have to write will be in ursa-visor, a gui coding language like blueprint but for GamePlus editor","Your game will be online","Your game will be offline","Graphics quality of your game will be low,you will be able to add lights but not too much and shadows will not be that 'real'","Graphics quality of your game will be medium, you will be able to add unlimited lights but lights will not be that 'real'","The best graphics quality be can provide","Will save the changed values in a file and apply them next time you open the editor"]
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = Tooltip(self.ToolTipList[i],z = -30,render_queue = 3,always_on_top = True)
                # self.ItemToToolTipList[i].tool_tip.background.z = -1

        else:
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = None

    def OpenProject(self,ProjectName,FuncToEnableOnOpen,FileName,FilePath):
        LoadProjectToScene(FileName = FileName,FilePath = FilePath,FuncToEnableOnOpen=FuncToEnableOnOpen)
        self.ProjectName = ProjectName
        self.UniversalParentEntity.disable()
        self._TempSavedItemOfRecentProject = self.EditorDataDictNonConfigable["RecentEdits"].pop(self.EditorDataDictNonConfigable["RecentEdits"].index(ProjectName))
        self.EditorDataDictNonConfigable["RecentEdits"].insert(0,self._TempSavedItemOfRecentProject)
        self.RegiveDataDictFunc(self.EditorDataDictConfigable,self.EditorDataDictNonConfigable)
        self.SaveNonConfiableData()

if __name__ == "__main__":
    app = Ursina()
    window.exit_button.disable()
    window.fps_counter.disable() 
    from GamePlusEditor.ursina.prefabs.memory_counter import MemoryCounter
    MemoryCounter()
    # window.fullscreen  = True
    from GamePlusEditor.OtherStuff import ScaleTransformer
    Ui = StartingUI(EditorDataDictConfigable={"Show tooltip":True,"Coordinates": 0},OnProjectStart=Func(print,"started"),ProjectName="PRoejcts1qe1234",SaveNonConfiableData=Func(print,"hi"),ShowInstructionFunc=Func(print_on_screen,"hi"),ChangeConfigDataToDefaultTypeFunc=Func(print_on_screen,"f"))
    Sky()
    Ui.Setup()
    def input(key):

        if key in {"w","w hold"}:
            Ui.SaveChangedVarsButton.y += .01
        if key in {"s","s hold"}:
            Ui.SaveChangedVarsButton.y -= .01
        if key in {"a","a hold"}:
            Ui.SaveChangedVarsButton.x -= .01
        if key in {"d","d hold"}:
            Ui.SaveChangedVarsButton.x += .01

        if key == "1":
            Ui.SaveChangedVarsButton.scale_x += .01
        if key == "2":
            Ui.SaveChangedVarsButton.scale_x -= .01
        if key == "3":
            Ui.SaveChangedVarsButton.scale_y += .01
        if key == "4":
            Ui.SaveChangedVarsButton.scale_y -= .01

        if key == "y":
            Ui.SaveChangedVarsButton.text = Ui.SaveChangedVarsButton.text

        if key == "p":
            print(Ui.SaveChangedVarsButton.position)

        # print(key)
    app.run()
