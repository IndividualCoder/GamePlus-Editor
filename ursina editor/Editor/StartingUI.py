from ursina import *

class StartingUI(Entity):
    def __init__(self):
        super().__init__(parent = camera.ui)
        
        self.StartingUIParentEntity = Entity(parent = self)
        self.RecentProjectsParentEntity = Entity(parent = self)

        self.CreateNewProjectButton = Draggable(parent = self.StartingUIParentEntity,text="Create new project",radius=.2,Key="c", on_key_press = self.CreateNewProject,on_click = self.CreateNewProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.384259, 0))
        self.ChangeVarsButton = Draggable(parent = self.StartingUIParentEntity,text="Change vars",radius=.2,Key="v", on_key_press = self.ChangeVars,on_click = self.ChangeVars,scale = (0.4,0.2),position = Vec3(0.56713, 0.384259, 0))
        self.LoadProjectButton = Draggable(parent = self.StartingUIParentEntity,text="Load project",radius=.2,Key="l", on_key_press = self.LoadProject,on_click = self.LoadProject,scale = (0.4,0.2),position = Vec3(-0.56713, 0.163194, 0))
        self.FourthButton = Draggable(parent = self.StartingUIParentEntity,text="Fourth one",radius=.2,Key="l", on_key_press = self.LoadProject,on_click = self.LoadProject,scale = (0.4,0.2),position = Vec3(0.56713, 0.163194, 0))

        self.ShowPos = Button(text="Show",radius=.2,Key="p", on_key_press = self.ShowPosTemp,on_click = self.ShowPosTemp,z = (10),scale = (0,0,0))

        self.BackgroundOfRecentProjects = Draggable(parent = self.RecentProjectsParentEntity,text = "H",color = color.gray,scale = Vec3(1.77292, 0.535418, 1),radius = 0,position = Vec3(-0.00231489, -0.232639, 0),)

    def ShowPosTemp(self):
        for i in range(len(self.StartingUIParentEntity.children)):
            print(self.StartingUIParentEntity.children[i].text,self.StartingUIParentEntity.children[i].position)
# ?        for i in range(len(self.RecentProjectsParentEntity.children)):
        print("pos",self.RecentProjectsParentEntity.children[0].position,"Scale",self.RecentProjectsParentEntity.children[0].scale)

    def CreateNewProject(self):
        pass

    def ChangeVars(self):
        pass

    def LoadProject(self):
        pass

if __name__ == "__main__":
    app = Ursina()


    Ui = StartingUI()
    Scale_x = Slider(min  = .1,max = 10,default=Ui.BackgroundOfRecentProjects.scale_x,dynamic=True)
    Scale_y = Slider(min  = .1,max = 10,default=Ui.BackgroundOfRecentProjects.scale_y,dynamic=True,y = .04)

    def ChangeValue():
        Ui.BackgroundOfRecentProjects.scale_x = Scale_x.value
        Ui.BackgroundOfRecentProjects.scale_y = Scale_y.value
    Scale_x.on_value_changed = ChangeValue
    Scale_y.on_value_changed = ChangeValue

    Sky()

    app.run()
