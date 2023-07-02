from ursina import *
from OtherStuff import CustomWindow

class StartingUI(Entity):
    def __init__(self):
        super().__init__(parent = camera.ui)
        
        self.UniversalParentEntity = Entity(parent = self)
        self.StartingUIParentEntity = Entity(parent = self.UniversalParentEntity)
        self.RecentProjectsParentEntity = Entity(parent = self.UniversalParentEntity)


        self.CreateNewProjectButton = Button(parent = self.StartingUIParentEntity,text="Create new project",radius=.2,Key="1", on_key_press = self.CreateNewProject,on_click = self.CreateNewProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.384259, 0))
        self.ChangeVarsButton = Button(parent = self.StartingUIParentEntity,text="Change vars",radius=.2,Key="2", on_key_press = self.ChangeVars,on_click = self.ChangeVars,scale = (0.4,0.2),position = Vec3(0.56713, 0.384259, 0))
        self.LoadProjectButton = Button(parent = self.StartingUIParentEntity,text="Load project",radius=.2,Key="3", on_key_press = self.LoadProject,on_click = self.LoadProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.163194, 0))
        self.QuitApplicationButton = Button(parent = self.StartingUIParentEntity,text="Close editor",radius=.2,Key="escape", on_key_press = self.CheckUserQuit,on_click = self.CheckUserQuit,scale = (0.4,0.2),position = Vec3(0.56713, 0.163194, 0))

        self.BackgroundOfRecentProjects = Entity(parent = self.RecentProjectsParentEntity,model = "cube",color = color.gray,scale = Vec3(1.77792, 0.535418, 0),position = Vec3(0, -0.232639, 0))


    def CreateNewProject(self):
        print_on_screen("Create new project",origin=(0,0),color=color.black66)

    def ChangeVars(self):
        print_on_screen("Change vars",origin=(0,0),color=color.black66)

    def LoadProject(self):
        print_on_screen("Load project",origin=(0,0),color=color.black66)

    def CheckUserQuit(self):
        CustomWindow(ToEnable=self.EnableEverything,OnEnable=self.DisableEverything,B1Key=["1" ,"space","n"],B2Key=["2","enter","y"])

    def DisableEverything(self):
        for i in range(len(self.UniversalParentEntity.children)):
            self.UniversalParentEntity.children[i].disable()

    def EnableEverything(self):
        self.UniversalParentEntity.enable()
        for i in range(len(self.UniversalParentEntity.children)):
            self.UniversalParentEntity.children[i].enable()

if __name__ == "__main__":
    app = Ursina()
    # window.fullscreen  = True

    Ui = StartingUI()

    Sky()

    app.run()
