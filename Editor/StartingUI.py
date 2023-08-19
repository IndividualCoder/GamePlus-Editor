from ursina import *
from OtherStuff import CustomWindow,ReplaceValue,PrepareForRecentProjects,CurrentFolderNameReturner
from ursina.prefabs.dropdown_menu import DropdownMenuButton
from CoreFiles.dropdown_menu import DropdownMenu as SimpleDropdownMenu
from RecentProjectFinder import GetRecentProjects
from ProjectLoader import LoadProjectToScene
# Dropdown menu fixing

class StartingUI(Entity):
    def __init__(self,NameOfChangeVarsList,TypeOfChangeVarsList,DefaultValueOfChangeVarsList,OnProjectStart,ExistingProjectsName,ProjectName,ProjectSettings={"ProjectGraphicsQuality": "Low","ProjectLanguage": "Python","ProjectNetworkingOnline": False,"CurrentTargatedPlatform": "windows","CurrentProjectBase": "FPC"}):
        super().__init__(parent = camera.ui)

        self.ProjectName = ProjectName
        self.ProjectSettings = ProjectSettings
        self.ExistingProjectsName = ExistingProjectsName
        self.NameVarsList = NameOfChangeVarsList
        self.TypeVarsList = TypeOfChangeVarsList
        self.ValueVarsList = DefaultValueOfChangeVarsList
        self.OnProjectStart = OnProjectStart
        self.ProjectDataName = ["ProjectGraphicsQuality","ProjectLanguage","ProjectNetworkingOnline","CurrentTargatedPlatform","CurrentProjectBase"]
        self.RecentProjectButtonTexts = ["Open project","Config project","Finish project","Delete project"]

        self.UniversalParentEntity = Entity(parent = self)
        self.StartingUIParentEntity = Entity(parent = self.UniversalParentEntity)
        self.RecentProjectsParentEntity = Entity(parent = self.StartingUIParentEntity)
        self.RecentProjectsScrollerParentEntity = Button(parent = self.StartingUIParentEntity,scale = Vec3(1.77792, 0.535418, 1),position = Vec3(0, -0.232639, 1),color = color.white,visible_self = True,radius=0)
        self.CreateNewProjectMenuParentEntity = Entity(parent = self.UniversalParentEntity,enabled = False)
        self.ChangeVarsMenuParentEntity = Entity(parent = self.UniversalParentEntity,enabled = False)
        self.ChangeVarsTextParentEntity = Entity(parent = self.ChangeVarsMenuParentEntity)

        self.CreateNewProjectButton = Button(parent = self.StartingUIParentEntity,text="Create new project",radius=.2,Key="1", on_key_press = self.ShowCreateNewProject,on_click = self.ShowCreateNewProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.384259, 0))
        self.ChangeVarsButton = Button(parent = self.StartingUIParentEntity,text="Change vars",radius=.2,Key="2", on_key_press = self.ChangeVarsMenu,on_click = self.ChangeVarsMenu,scale = (0.4,0.2),position = Vec3(0.56713, 0.384259, 0))
        self.LoadProjectButton = Button(parent = self.StartingUIParentEntity,text="Load project",radius=.2,Key="3", on_key_press = self.LoadProject,on_click = self.LoadProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.163194, 0))
        self.QuitApplicationButton = Button(parent = self.StartingUIParentEntity,text="Close editor",radius=.2,Key=["escape",'4'], on_key_press = self.CheckUserQuit,on_click = self.CheckUserQuit,scale = (0.4,0.2),position = Vec3(0.56713, 0.163194, 0))

        self.BackgroundOfRecentProjects = Entity(parent = self.RecentProjectsParentEntity,model = "cube",color = color.gray,scale = Vec3(1.77792, 0.535418, 0),position = Vec3(0, -0.232639, 0))

        self.LineOnTop = Entity(name = "LineOnTop",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = 5,position = Vec3(0, 0.405, -10),color = color.gray,z = -10)
        self.LineBetweenTypeAndInputFieldLine = Entity(name = "LineBetweenTypeAndInputFieldLine",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = len(self.NameVarsList),rotation_z = 90,position = Vec3(0.03, 0, -10),color = color.gray,z = -10)
        self.LineBetweenInputFieldAndDescriptionLine = Entity(name = "LineBetweenInputFieldAndDescriptionLine",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = len(self.NameVarsList),rotation_z = 90,position = Vec3(0.375, 0, -10),color = color.gray,z = -10)
        self.GoBackOfChangeVarsMenuButton = Button(name = "Go Back Of Change Vars Menu Button",parent = self.ChangeVarsMenuParentEntity,text="Done",Key="escape",on_click = Sequence(Func(self.DestroyChangeVarsMenuButtons),Func(self.ChangeVarsMenuParentEntity.disable),Func(self.EnableStaringUI)),radius=0,scale = Vec3(0.280001, 0.0800007, 1),position = Vec3(-0.744999, 0.455, 0))
        self.LineBetweenNameAndTypeLine = Entity(name = "LineBetweenNameAndTypeLine",parent = self.ChangeVarsMenuParentEntity,model = "line",scale = len(self.NameVarsList),rotation_z = 90,position = (-.38,0),color = color.gray,z = -10)
        self.BackgroundOfChangeVarsMenu = Entity(parent = self.ChangeVarsMenuParentEntity,model = "cube",color = color.rgba(0,0,0,200),scale = Vec3(10,10, 0),position = Vec3(0, 0, 0))

        self.CreateNewProjectFpcButton = Button(name = "FPC",parent = self.CreateNewProjectMenuParentEntity,text="FPC\nFirst person controller",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (-0.68, 0.3, 0),on_click = Func(self.CreateNewProject,"FPC"),Key = "1",on_key_press=Func(self.CreateNewProject,"FPC"),color = color.red) #Game is based on First person controller (3d)
        self.CreateNewProjectTpcButton = Button(name = "TPC",parent = self.CreateNewProjectMenuParentEntity,text="TPC\nThird person controller",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (-0.37, 0.3, 0),on_click = Func(self.CreateNewProject,"TPC"),Key = "2",on_key_press=Func(self.CreateNewProject,"TPC")) #Game is based on Third person controller (3d)
        self.CreateNewProjectTopDownButton = Button(name = "Top down",parent = self.CreateNewProjectMenuParentEntity,text="Top-Down\nTop-down game (3d)",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (-0.06, 0.3, 0),on_click = Func(self.CreateNewProject,"TopDown"),Key = "3",on_key_press=Func(self.CreateNewProject,"TopDown")) #Game is based on Top-Down made (2d)
        self.CreateNewProjectPlatformerButton = Button(name = "2d",parent = self.CreateNewProjectMenuParentEntity,text="Platformer\n2d platformer",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (0.25, 0.3, 0),on_click = Func(self.CreateNewProject,"Platformer"),Key = "4",on_key_press=Func(self.CreateNewProject,"Platformer")) #Game is based on  platformer mode (2d)
        self.CreateNewProjectFpcAndTpcButton = Button(name = "FPC/TPC",parent = self.CreateNewProjectMenuParentEntity,text="FPC/TPC\nBoth Fpc and Tpc",radius = 0,enabled = False,scale = (0.27, 0.23, 1),position = (0.56, 0.3, 0),on_click = Func(self.CreateNewProject,"FPCTPC"),Key = "5",on_key_press=Func(self.CreateNewProject,"FPCTPC")) #Game is based on both FPC and TPC
        self.CreateNewProjectBaseDict = {"FPC": self.CreateNewProjectFpcButton,"TPC": self.CreateNewProjectTpcButton,"TopDown": self.CreateNewProjectTopDownButton,"Platformer": self.CreateNewProjectPlatformerButton,"FPCTPC": self.CreateNewProjectFpcAndTpcButton} # Made a dict to avoid multiple if
        self.CurrentProjectBase = self.CreateNewProjectBaseDict["FPC"]

        self.ProjectTitleButton = InputField(name = "Title input field",parent = self.CreateNewProjectMenuParentEntity,placeholder="Enter your project's title",enabled = False,active = False,position = (-.485,.15),origin_x = 0,radius = 0,scale = (.66,.05),submit_on="enter")

        self.LanguageText = Text(name = "Select project language text",parent = self.CreateNewProjectMenuParentEntity,text="Language",position = (-0.8, 0.105, 0),scale = 1) #-0.81, 0.09, 0
        self.LanguageText.create_background(.03,0)
        self.LanguageMenuParentEntity = Entity(name = "Language parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = (.3,.2),enabled = False,position = (-0.664, -.040,1))
        self.LanguagePythonButton = Button(parent = self.LanguageMenuParentEntity,text = "Python",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (.7,.3),enabled = False,position = (.15,-.214,-1),radius = 0,on_click = self.SetProjectLanguage)
        self.LanguageUrsaVisorButton = Button(parent = self.LanguageMenuParentEntity,text = "Ursa-visor",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (.7,.3),enabled = False,position = (-.15,.214,-1),radius = 0,on_click = self.SetProjectLanguage)

        self.TargatedPlatformText = Text(name = "Select project targated platform text",parent = self.CreateNewProjectMenuParentEntity,text="Targated platform",position = (-0.485, 0.105, 0),scale = 1)
        self.TargatedPlatformText.create_background(.03,0)
        self.TargatedPlatformDropdownMenu =     SimpleDropdownMenu(name = "Dropdown menu",parent = self.CreateNewProjectMenuParentEntity,text = 'Widnows',color = color.blue,highlight_color = color.blue.tint(.2),on_click = Func(self.SetProjectTargatedPlatform,"windows"), buttons=(DropdownMenuButton(name = 'Android',text="Android",color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"android")),DropdownMenuButton('Mac',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"mac")),DropdownMenuButton('ios',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"ios")),DropdownMenuButton('Linux',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"linux"))),click_to_open=True,position = (-.5,0.06),scale = (.25,0.025))
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
        self.StartProjectButton = Button(name = "Start button of create new project menu",parent = self.CreateNewProjectMenuParentEntity,text="Start",Key = "enter",scale = (.3,.25),on_click = Sequence(Func(invoke,self.StartProject,delay = .1),Func(invoke,self.SetProjectName,delay = .15)))

        # self.TempButton  = Button(scale = (0,0),Key="o",on_key_press=self.ShowPosTemp)

        # self.TempButton3 = Button(scale = (0,0),Key=["a","a hold"],on_key_press=self.ChangeTitleFieldPositionXN)
        # self.TempButton4 = Button(scale = (0,0),Key=["d","d hold"],on_key_press=self.ChangeTitleFieldPositionXP)
        # self.TempButton5 = Button(scale = (0,0),Key=["w","w hold"],on_key_press=self.ChangeTitleFieldPositionYP)
        # self.TempButton6 = Button(scale = (0,0),Key=["s","s hold"],on_key_press=self.ChangeTitleFieldPositionYN)

        # self.TempButton7 = Button(scale = (0,0),Key=["left arrow","left arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionXN)
        # self.TempButton8 = Button(scale = (0,0),Key=["right arrow","right arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionXP)
        # self.TempButton9 = Button(scale = (0,0),Key=["up arrow","up arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionYP)
        # self.TempButton10 = Button(scale = (0,0),Key=["down arrow","down arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionYN)

        # self.TempButton11 = Button(scale = (0,0),Key=["z","z hold"],on_key_press=self.ChangeDescriptionFieldPositionXN2)
        # self.TempButton12 = Button(scale = (0,0),Key=["x","x hold"],on_key_press=self.ChangeDescriptionFieldPositionXP2)
        # self.TempButton13 = Button(scale = (0,0),Key=["c","c hold"],on_key_press=self.ChangeDescriptionFieldPositionYP2)
        # self.TempButton14 = Button(scale = (0,0),Key=["v","v hold"],on_key_press=self.ChangeDescriptionFieldPositionYN2)

        # self.TempButton15  = Button(scale = (0,0),Key=["5","5 hold"],on_key_press=self.ScaleUpX)
        # self.TempButton16  = Button(scale = (0,0),Key=["6","6 hold"],on_key_press=self.ScaleUpY)
        # self.TempButton17  = Button(scale = (0,0),Key=["7","7 hold"],on_key_press=self.ScaleUpX2)
        # self.TempButton18  = Button(scale = (0,0),Key=["8","8 hold"],on_key_press=self.ScaleUpY2)

        # self.TempButton19  = Button(scale = (0,0),Key=["5","5 hold"],on_key_press=self.ScaleUpX3)
        # self.TempButton20  = Button(scale = (0,0),Key=["6","6 hold"],on_key_press=self.ScaleUpY3)
        # self.TempButton21  = Button(scale = (0,0),Key=["7","7 hold"],on_key_press=self.ScaleUpX4)
        # self.TempButton22  = Button(scale = (0,0),Key=["8","8 hold"],on_key_press=self.ScaleUpY4)

    def ShowPosTemp(self):
        for i in range(len(self.RecentProjectsScrollerParentEntity.children)):
            print(f'name: {self.RecentProjectsScrollerParentEntity.children[i].name},pos:{self.RecentProjectsScrollerParentEntity.children[i].position},Scale:{self.RecentProjectsScrollerParentEntity.children[i].scale}')

    def ScaleUpX(self):
        # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
        self.RecentProjectsScrollerParentEntity.children[1].scale_x -= .01

    def ScaleUpY(self):
        # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
        self.RecentProjectsScrollerParentEntity.children[1].scale_y -= .01

    def ScaleUpX2(self):
        # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
        self.RecentProjectsScrollerParentEntity.children[1].scale_x += .01

    def ScaleUpY2(self):
        # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
        self.RecentProjectsScrollerParentEntity.children[1].scale_y += .01

    # def ScaleUpX3(self):
    #     # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    #     self.ProjectGraphicsQualityMediumButton.x -= .01

    # def ScaleUpY3(self):
    #     # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    #     self.ProjectGraphicsQualityMediumButton.y -= .01

    # def ScaleUpX4(self):
    #     # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    #     self.ProjectGraphicsQualityMediumButton.x += .01

    # def ScaleUpY4(self):
    #     # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    #     self.ProjectGraphicsQualityMediumButton.y += .01


    def ChangeTitleFieldPositionXP(self):
        self.RecentProjectsText.x += .005

    def ChangeTitleFieldPositionXN(self):
        self.RecentProjectsText.x -= .005

    def ChangeTitleFieldPositionYP(self):
        self.RecentProjectsText.y += .005

    def ChangeTitleFieldPositionYN(self):
        self.RecentProjectsText.y -= .005


    def ChangeDescriptionFieldPositionXP(self):
        self.RecentProjectsScrollerParentEntity.children[1].x += .001

    def ChangeDescriptionFieldPositionXN(self):
        self.RecentProjectsScrollerParentEntity.children[1].x -= .001

    def ChangeDescriptionFieldPositionYP(self):
        self.RecentProjectsScrollerParentEntity.children[1].y += .001

    def ChangeDescriptionFieldPositionYN(self):
        self.RecentProjectsScrollerParentEntity.children[1].y -= .001


    def ChangeDescriptionFieldPositionXP2(self):
        self.ProjectGraphicsQualityHighButton.x += .01

    def ChangeDescriptionFieldPositionXN2(self):
        self.ProjectGraphicsQualityHighButton.x -= .01

    def ChangeDescriptionFieldPositionYP2(self):
        self.ProjectGraphicsQualityHighButton.y += .01

    def ChangeDescriptionFieldPositionYN2(self):
        self.ProjectGraphicsQualityHighButton.y -= .01



    def ShowCreateNewProject(self):
        self.DisableStartingUI()
        self.EnableCreateNewProjectMenuButtons()
        self.EnableLanguageButtons()
        self.EnableNetworkingButtons()
        self.EnableGraphicsQualityButtons()
        invoke(self.ProjectTitleButton.MakeActive,delay = .1)


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
            if self.ProjectTitleButton.text.replace(" ","") == "":
                print_on_screen("Enter your project's name.",color = color.red,origin = (0,0),duration=3,position = (.5,-.1),scale = 1.2)
                return

            elif self.ProjectTitleButton.text in self.ExistingProjectsName:
                print_on_screen("You already have a project with this name.\nChoose a new one",color = color.red,origin = (0,0),duration=3,position = (.5,-.1),scale = 1.2)
                return

            self.CreateNewProjectMenuParentEntity.disable()

            self.OnProjectStart()


    def ChangeVarsMenu(self):
        self.ChangeVarsTextParentEntity.enable()
        self.DisableStartingUI()
        for i in range(len(self.NameVarsList)*2):
            if i % 2 == 0:
                self.ChangeVarsTextParentEntity.children.append(Text(name = f"Change var children_{i}",text=self.NameVarsList[int(i/2)],parent  = self.ChangeVarsTextParentEntity,position = (-.87,.39-i/2*0.07,-10),scale = 1.75)) 
            else:
                self.ChangeVarsTextParentEntity.children.append(Entity(name = f"Line_{i}",parent = self.ChangeVarsTextParentEntity,model = "line",scale = 2,position = (0,.37-i/2*0.07),color = color.gray,z = -10)) 


        if len(self.TypeVarsList) < len(self.NameVarsList):
            for i in range(len(self.NameVarsList)-len(self.TypeVarsList)):
                self.TypeVarsList.append("Unknown")

        if len(self.ValueVarsList) < len(self.NameVarsList):
            for i in range(len(self.NameVarsList) - len(self.ValueVarsList)):
                self.ValueVarsList.append("None")

        for i in range(len(self.TypeVarsList)):
            self.ChangeVarsTextParentEntity.children.append(Text(name = f"change var type {i}",parent=self.ChangeVarsTextParentEntity,text=self.TypeVarsList[i].capitalize(),position = Vec3(-0.37, 0.39-i*0.07, -10),scale = 1.75))

        for i in range(len(self.ValueVarsList)):
            self.ChangeVarsTextParentEntity.children.append(InputField(name = f"Input field_{i}",parent = self.ChangeVarsTextParentEntity,default_value=str(self.ValueVarsList[i]),position = Vec3(0.2, 0.37-i*0.07, -10),scale = Vec3(0.32, 0.05, 1),active = False,escape_active=True))


            # print(self.ValueVarsList[i])
        


            # print(type(self.TypeVarsList[i]))

        self.EnableChangeVarsMenuButtons()

    def DestroyChangeVarsMenuButtons(self):
        self.TempVar = len(self.ChangeVarsTextParentEntity.children)
        # print(self.TempVar)
        for i in range(self.TempVar - 1, -1, -1):
            # del self.ChangeVarsTextParentEntity.children[i]
            destroy(self.ChangeVarsTextParentEntity.children[i])

        del self.TempVar


    def LoadProject(self):
        print_on_screen("Load project",origin=(0,0),color=color.black66)

    def CheckUserQuit(self):
        invoke(CustomWindow,ToEnable=self.EnableEverything,OnEnable=self.DisableEverything,B1Key=["1" ,"escape"],B2Key=["2","enter"],delay = .1)


    def ShowRecentProjects(self,List):
        self.RecentProjectsText = Text(name = "RecentProjectsText",parent = self.RecentProjectsParentEntity,text = "Recent projects",position = Vec3(-0.879999, 0.025, 0),scale = 1.5)
        self.RecentProjectsLine = Entity(name = "RecentProjectsLine",parent = self.RecentProjectsParentEntity,model = "line",position = Vec3(0, -0.02, 0),scale = Vec3(1.78, 0.85, 1))
        self.TotalRunningProjects = self.LoadRecentProjects()
        self.SetRecentProjects(self.TotalRunningProjects,List)
        # print(rece)
        # print(self.LoadRecentProjects())

    def LoadRecentProjects(self,ReturnOrder = None):
        CurrentFolderName = CurrentFolderNameReturner()
        # print("mine",CurrentFolderName)
        CurrentFolderName = CurrentFolderName.replace("\\","/")
        CurrentFolderName = CurrentFolderName.replace("Editor","Current Games")
        # print("mine : ",Pathh)

        # print(CurrentFolderName)
        return GetRecentProjects(CurrentFolderName,order=ReturnOrder)

    def SetRecentProjects(self,ProjectSettings,List):
        # print(ProjectSettings," THis is")
        for i in range(len(ProjectSettings)):
            Text(parent = self.RecentProjectsScrollerParentEntity,text=list(ProjectSettings)[i],position = Vec3(-0.492997-i*-0.3, 0.366999, 0),scale = Vec3(0.73, 2.39, 1),always_on_top = True)
            Entity(parent = self.RecentProjectsScrollerParentEntity,model = "line",position = Vec3(-0.2-i*-0.3, -0.0529997, 0),scale = Vec3(0.899999, 0.2, 0.1),rotation_z = 90,always_on_top = True)


            currentPro = ProjectSettings[list(ProjectSettings)[i]]
            for j in range(len(self.ProjectDataName)):
                Text(parent = self.RecentProjectsScrollerParentEntity,text=f"{PrepareForRecentProjects(self.ProjectDataName[j])}: {currentPro[list(currentPro)[j]]}",position = Vec3(-0.492997-i*-0.3, 0.27-j*.07, 0),scale = Vec3(0.63, 2.19, 1),always_on_top = True)

            for k in range(int(len(self.RecentProjectButtonTexts)/2)):
            # Button(parent = self.RecentProjectsScrollerParentEntity,text=f"{self.RecentProjectButtonTexts[int(k/2)]}1",color = color.blue,scale = Vec3(0.12,.1,1),position = Vec3(-0.43-i*-.3,-.15,0))
                Button(parent = self.RecentProjectsScrollerParentEntity,text=f"{self.RecentProjectButtonTexts[int(k)]}",color = color.blue,scale = Vec3(0.12,.1,1),position = Vec3(-0.43-i*-.3+k*.15,-.15,-1),always_on_top = True,on_click = Func(self.OpenProject,FileName = list(ProjectSettings)[i],FilePath = CurrentFolderNameReturner().replace("Editor","Current Games"),List = List,ProjectName = list(ProjectSettings)[i]))

            for l in range(int(len(self.RecentProjectButtonTexts)/2),len(self.RecentProjectButtonTexts)):
            # # Button(parent = self.RecentProjectsScrollerParentEntity,text=f"{self.RecentProjectButtonTexts[int(k/2)]}1",color = color.blue,scale = Vec3(0.12,.1,1),position = Vec3(-0.43-i*-.3,-.3,0))
                Button(parent = self.RecentProjectsScrollerParentEntity,text=f"{self.RecentProjectButtonTexts[int(l)]}",color = color.blue,scale = Vec3(0.12,.1,1),position = Vec3(-0.43-i*-.3-l*.15,-.3,-1),always_on_top = True,on_click = Func(self.OpenProject,FileName = list(ProjectSettings)[i],FilePath = CurrentFolderNameReturner().replace("Editor","Current Games"),List = List,ProjectName = list(ProjectSettings)[i]))
                # print(list(ProjectSettings)[i])

            # print(ProjectSettings)

        Entity(parent = self.RecentProjectsScrollerParentEntity,model = "line",position = Vec3(-0.349999, 0.298, 0),scale = len(ProjectSettings))
        self.RecentProjectsScrollerParentEntity.add_script(Scrollable(max = -.001,axis = 'x',scroll_speed = .01))


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
        self.UiData = dict(zip(self.NameVarsList, self.ValueVarsList))
        self.SetTooltip(self.UiData["Show tooltip"])
            
    def SetTooltip(self,value):
        if value:
            self.ToolTipList = ["First person games like valorant, cod etc","Third person games like pubg, gta etc","Camera is stuck at one place but not in 2d, this category is also called '2.5d games',like clash of clans, clash royale etc","2d game where camera is stuck at one place in 2d","Both TPC and FPC","If enabled,the little amount to code you will have to write will be in python","If enabled,the little amount to code you will have to write will be in ursa-visor, a gui coding language like blueprint but for ursina editor","Your game will be online","Your game will be offline","Graphics quality of your game will be low,you will be able to add lights but not too much and shadows will not be that 'real'","Graphics quality of your game will be medium, you will be able to add unlimited lights but lights will not be that 'real'","The best graphics quality be can provide"]
            self.ItemToToolTipList = [self.CreateNewProjectFpcButton,self.CreateNewProjectTpcButton,self.CreateNewProjectTopDownButton,self.CreateNewProjectPlatformerButton,self.CreateNewProjectFpcAndTpcButton,self.LanguagePythonButton,self.LanguageUrsaVisorButton,self.ProjectNetworkignOnlineButton,self.ProjectNetworkignOfflineButton,self.ProjectGraphicsQualityLowButton,self.ProjectGraphicsQualityMediumButton,self.ProjectGraphicsQualityHighButton]
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = Tooltip(self.ToolTipList[i],z = -10)
                # self.ItemToToolTipList[i].tool_tip.background.z = -1

        else:
            self.ItemToToolTipList = [self.CreateNewProjectFpcButton,self.CreateNewProjectTpcButton,self.CreateNewProjectTopDownButton,self.CreateNewProjectPlatformerButton,self.CreateNewProjectFpcAndTpcButton,self.LanguagePythonButton,self.LanguageUrsaVisorButton,self.ProjectNetworkignOnlineButton,self.ProjectNetworkignOfflineButton,self.ProjectGraphicsQualityLowButton,self.ProjectGraphicsQualityMediumButton,self.ProjectGraphicsQualityHighButton]
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = None

    def OpenProject(self,ProjectName,List,FileName,FilePath):
        LoadProjectToScene(FileName = FileName,FilePath = FilePath,List=List)
        self.ProjectName = ProjectName
        print("helo")
        self.OnProjectStart()
        self.UniversalParentEntity.disable()

if __name__ == "__main__":
    app = Ursina()
    window.exit_button.disable()
    window.fps_counter.disable() 
    from ursina.prefabs.memory_counter import MemoryCounter
    MemoryCounter()
    # window.fullscreen  = True
    from OtherStuff import ScaleTransformer
    Ui = StartingUI(NameOfChangeVarsList=["Text 1","Text 2","Text 3","Text 1","Text 2","Text 3"],TypeOfChangeVarsList=["int","float","bool"],DefaultValueOfChangeVarsList = ["755",5.8,False,"yes"],OnProjectStart=Func(print,"started"),ExistingProjectsName=["pro"],ProjectName="PRoejcts1qe1234")
    Sky()
    Ui.ShowRecentProjects()
    def input(key):
        if key == "p":
            Ui.RecentProjectsScrollerParentEntity.visible = not Ui.RecentProjectsScrollerParentEntity.visible
        if key == "0":
            Ui.SetTooltip(True)
        elif key == "1":
            Ui.SetTooltip(False)

        # print(key)
    app.run()
