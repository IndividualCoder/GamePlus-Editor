from ursina import *
from OtherStuff import CustomWindow,ReplaceValue,Replacer
from ursina.prefabs.dropdown_menu import DropdownMenuButton
from CoreFiles.dropdown_menu import DropdownMenu as SimpleDropdownMenu
# Dropdown menu fixing

class StartingUI(Entity):
    def __init__(self,NameOfChangeVarsList,TypeOfChangeVarsList,DefaultValueOfChangeVarsList,OnProjectStart,ExistingProjectsName):
        super().__init__(parent = camera.ui)

        self.ProjectLanguage = "python"
        self.ProjectBase = "FPC"
        self.ProjectNetworkingOnline = False
        self.ProjectGraphicsQuality = "Medium"
        self.ExistingProjectsName = ExistingProjectsName
        self.NameVarsList = NameOfChangeVarsList
        self.TypeVarsList = TypeOfChangeVarsList
        self.ValueVarsList = DefaultValueOfChangeVarsList
        self.OnProjectStart = OnProjectStart

        self.UniversalParentEntity = Entity(parent = self)
        self.StartingUIParentEntity = Entity(parent = self.UniversalParentEntity)
        self.RecentProjectsParentEntity = Entity(parent = self.StartingUIParentEntity)
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
        self.LanguageMenuParentEntity = Entity(name = "Language parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = (.3,.2),enabled = False,position = (-0.664, -.040,-60))
        self.LanguagePythonButton = Button(parent = self.LanguageMenuParentEntity,text = "Python",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (.7,.3),enabled = False,position = (.15,-.214),radius = 0,always_on_top = True,on_click = self.SetProjectLanguage)
        self.LanguageBlueprintButton = Button(parent = self.LanguageMenuParentEntity,text = "Blueprint",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (.7,.3),enabled = False,position = (-.15,.214),radius = 0,always_on_top = True,on_click = self.SetProjectLanguage)

        self.TargatedPlatformText = Text(name = "Select project targated platform text",parent = self.CreateNewProjectMenuParentEntity,text="Targated platform",position = (-0.485, 0.105, 0),scale = 1)
        self.TargatedPlatformText.create_background(.03,0)
        self.TargatedPlatformDropdownMenu =     SimpleDropdownMenu(name = "Dropdown menu",parent = self.CreateNewProjectMenuParentEntity,text = 'Widnows',color = color.blue,highlight_color = color.blue.tint(.2),on_click = Func(self.SetProjectTargatedPlatform,"windows"), buttons=(DropdownMenuButton('Android',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"android")),DropdownMenuButton('Mac',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"mac")),DropdownMenuButton('ios',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"ios")),DropdownMenuButton('Linux',color = color.green,highlight_color = color.green.tint(-.2),on_click = Func(self.SetProjectTargatedPlatform,"linux"))),click_to_open=True,position = (-.5,0.06),scale = (.25,0.025))
        self.TargatedPlatformBaseDict = {"windows": self.TargatedPlatformDropdownMenu,"android": self.TargatedPlatformDropdownMenu.buttons[0],"mac": self.TargatedPlatformDropdownMenu.buttons[1],"ios": self.TargatedPlatformDropdownMenu.buttons[2],"linux": self.TargatedPlatformDropdownMenu.buttons[3]}
        self.CurrentTargatedPlatform = self.TargatedPlatformBaseDict["windows"]

        self.ProjectNetworkingText = Text(name = "Select project networking text",parent = self.CreateNewProjectMenuParentEntity,text="Networking",position = (-0.8, -0.1649999, 0),scale = 1)
        self.ProjectNetworkingText.create_background(.03,0)
        self.ProjectNetworkingMenuParentEntity = Entity(name = "Networking parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = (.3,.2),enabled = False,position = (-0.664, -.31,60))
        self.ProjectNetworkignOnlineButton = Button(parent = self.ProjectNetworkingMenuParentEntity,text = "Offline",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (1,.3),enabled = False,position = (0,-.214,-20),radius = 0,always_on_top = True,on_click = self.SetProjectNetworking)
        self.ProjectNetworkignOfflineButton = Button(parent = self.ProjectNetworkingMenuParentEntity,text = "Online",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (1,.3),enabled = False,position = (0,.214,-20),radius = 0,always_on_top = True,on_click = self.SetProjectNetworking)

        self.ProjectGraphicsQualityText = Text(name = "Select project graphics quality text",parent = self.CreateNewProjectMenuParentEntity,text="Select graphics quality",position = (-0.49, -0.1, 0),scale = 1)
        self.ProjectGraphicsQualityText.create_background(.03,0)
        self.ProjectGraphicsQualityMenuParentEntity = Entity(name = "Graphics parent",parent = self.CreateNewProjectMenuParentEntity,model = "cube",color = color.dark_gray,scale = Vec3(0.3, 0.26, 1),enabled = False,position = (-0.354, -0.28, 60))

        self.ProjectGraphicsQualityLowButton = Button(name = "Low",parent = self.ProjectGraphicsQualityMenuParentEntity,text = "Low",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (1,.25),enabled = False,position = (0,.336667,-20),radius = 0,always_on_top = True,on_click = Func(self.SetProjectGraphicsQuality,"Low"))
        self.ProjectGraphicsQualityMediumButton = Button(name = "Medium",parent = self.ProjectGraphicsQualityMenuParentEntity,text = "Medium",color = color.blue,highlight_color = color.blue.tint(-.2),clicked_color = color.blue,scale = (1,.25),enabled = False,position = (0,.0033333,-20),radius = 0,always_on_top = True,on_click = Func(self.SetProjectGraphicsQuality,"Medium"))
        self.ProjectGraphicsQualityHighButton = Button(name = "High",parent = self.ProjectGraphicsQualityMenuParentEntity,text = "High (AAA)",color = color.light_gray.tint(-.2),highlight_color = color.light_gray,clicked_color = color.blue,scale = (1,.25),enabled = False,position = (0,-.33,-20),radius = 0,always_on_top = True,on_click = Func(self.SetProjectGraphicsQuality,"High"))
        self.CurrentGraphicsQuality = self.ProjectGraphicsQualityMediumButton
        self.StartProjectButton = Button(name = "Start button of create new project menu",parent = self.CreateNewProjectMenuParentEntity,text="Start",Key = "enter",scale = (.3,.25),on_click = Func(invoke,self.StartProject,delay = .1))


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
            print_on_screen(NewProjectBase,origin=(0,0,0),color=color.black,duration=1)
            # self.CreateNewProjectFpcButton.color = color.blue.tint(-.4)
            self.CurrentProjectBase = self.CreateNewProjectBaseDict[NewProjectBase]

    def SetProjectLanguage(self):
        ReplaceValue(self.LanguagePythonButton,self.LanguageBlueprintButton)
        ReplaceValue(self.LanguagePythonButton,self.LanguageBlueprintButton,"highlight_color")

        if self.ProjectLanguage == "blueprint":
            self.ProjectLanguage = "python"
        else:
            self.ProjectLanguage = "blueprint"

        print(self.ProjectLanguage)

    def SetProjectTargatedPlatform(self,New):
        try:
            ReplaceValue(self.TargatedPlatformBaseDict[New],self.CurrentTargatedPlatform,"text")
            ReplaceValue(self.TargatedPlatformBaseDict[New],self.CurrentTargatedPlatform,"text_entity")
            # ReplaceValue(self.TargatedPlatformBaseDict[New],self.CurrentTargatedPlatform,"on_click")
            self.CurrentTargatedPlatform = self.TargatedPlatformBaseDict[New]
        except:
            print_on_screen("An error occured. Rerminating function")

    def SetProjectNetworking(self):
        ReplaceValue(self.ProjectNetworkignOfflineButton,self.ProjectNetworkignOnlineButton)
        ReplaceValue(self.ProjectNetworkignOfflineButton,self.ProjectNetworkignOnlineButton,"highlight_color")

        self.ProjectNetworkingOnline = not self.ProjectNetworkingOnline

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

        self.ProjectGraphicsQuality = New
        # print(self.ProjectGraphicsQuality)

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
        invoke(CustomWindow,ToEnable=self.EnableEverything,OnEnable=self.DisableEverything,B1Key=["1" ,"escape","n"],B2Key=["2","enter","y"],delay = .1)

    def LoadRecentProjects(self):
        pass

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


if __name__ == "__main__":
    app = Ursina()
    window.exit_button.disable()
    window.fps_counter.disable() 
    from ursina.prefabs.memory_counter import MemoryCounter
    MemoryCounter()
    # window.fullscreen  = True
    from OtherStuff import ScaleTransformer
    Ui = StartingUI(NameOfChangeVarsList=["Text 1","Text 2","Text 3","Text 1","Text 2","Text 3"],TypeOfChangeVarsList=["int","float","bool"],DefaultValueOfChangeVarsList = ["755",5.8,False,"yes"],OnProjectStart=Func(print,"started"),ExistingProjectsName=["pro"])
    Sky()
    def input(key):
        print(key)
    app.run()
