from ursina import *
from ursina.color import tint
from OtherStuff import CustomWindow
from SceneEditor import SceneEditor

class ProjectEditor(Entity):
    def __init__(self,ExportToPyFunc,CurrentTabs,EditorCamera,cam = camera,enabled = True,**kwargs):
        super().__init__(kwargs)
        self.ExportToPyFunc = ExportToPyFunc
        self.CurrnetTabs = CurrentTabs
        self.EditorCamera = EditorCamera
        self.IsEditing = True
        self.enabled = enabled

        self.UniversalParentEntity = Entity(parent = cam.ui,enabled = self.enabled)
        self.TopButtonsParentEntity = Entity(parent = self.UniversalParentEntity,enabled = self.enabled,model = "cube",color = tint(color.white,-.6),texture ="white_cube",position  = (window.top[0],window.top[1] - .03,0) ,scale =(window.screen_resolution[0] / 1052,window.screen_resolution[1]/18000,2),always_on_top = True)
        self.TabsMenuParentEntity = Button(parent  = self.UniversalParentEntity,enabled = self.enabled,model = "cube",color = color.green,position  = Vec3(0, 0.5, -20) ,scale = Vec3(1.78, 0.1, 1),always_on_top = True,render_queue = -1,Key = "tab",on_key_press=self.ShowTabMenu) # Vec3(0, 0.39, 1) animate


        self.SaveProjectButton = Button(parent = self.TopButtonsParentEntity,text="Save",color = color.blue,radius  = 0,position =(-0.437, 0, -1),scale = (1/11,0.7)) #Vec3(0.179, 0.0385, 1)
        self.FinishProjectButton = Button(parent = self.TopButtonsParentEntity,text="Finish",color = color.blue,radius  = 0,position =(-0.337, 0, -1),scale = (1/11,0.7),on_click = self.FinishProject) #Vec3(0.179, 0.0385, 1)
        self.PlayProjectButton = Button(parent = self.TopButtonsParentEntity,text="Play",color = color.blue,radius  = 0,position =(-0.237, 0, -1),scale = (1/11,0.7)) #Vec3(0.179, 0.0385, 1)


    def FinishProject(self):
        invoke(self.ShowCustomWindow,ToEnable = self.CancelFinishingProject,Title = "Export to py",OnEnable = self.ShowFinishProjectMenu,
               CalcAndAddTextLines = False,ToAddHeight = 3,
               Content = [Text("Note: You can later export the project to cpp.\nWhen it is implemented ;)\n\nNote: There will be a folder named 'Exported games'\n           in your current dir and your game will be saved in\n           that folder in a .py format."),
                          Button(color = color.rgba(255,255,255,125),text  = "Export to py",highlight_color = color.blue,on_click = self.ExportToPy),
                          Button(color = color.rgba(255,255,255,125),text  = "Cancel",highlight_color = color.blue,click_to_destroy = True)],
                          delay = .1)


    def ShowFinishProjectMenu(self):
        self.EditorCamera.disable()
        for i in range(len(self.CurrnetTabs)):
            if isinstance(self.CurrnetTabs,SceneEditor):
                self.CurrnetTabs[i].IsEditing = False

    def ExportToPy(self):
        self.ExportToPyFunc()

    def CancelFinishingProject(self):
        self.EditorCamera.enable()
        for i in range(len(self.CurrnetTabs)):
            if isinstance(self.CurrnetTabs,SceneEditor):
                self.CurrnetTabs[i].IsEditing = True

    def EnableEditor(self,EditorsOldestAncestor):
        EditorsOldestAncestor.enable()
        for i in range(len(EditorsOldestAncestor.children)):
            EditorsOldestAncestor.children[i].enable()
            if len(EditorsOldestAncestor.children[i].children) > 0:
                self.EnableEditor(EditorsOldestAncestor.children[i])

    def ShowCustomWindow(self,ToEnable,OnEnable,Title = "Info",CalcAndAddTextLines  = True,ToAddHeight = 0,Content = None):
        self.CurrentCustomWindow = CustomWindow(ToEnable=ToEnable,title = Title,OnEnable=OnEnable,
                CalcAndAddTextLines = CalcAndAddTextLines,ToAddHeight = ToAddHeight,content = Content)

    def ShowTabMenu(self):
        # print("yes")
        if self.IsEditing:
            if not held_keys["control"] and not held_keys["shift"] and not held_keys["alt"]:
                if round(self.TabsMenuParentEntity.y,2) == 0.39:
                    self.TabsMenuParentEntity.animate_position(Vec3(0, 0.5, 0),.5)
                else:
                    self.TabsMenuParentEntity.animate_position(Vec3(0, 0.39, 0),.5)

    # def input(self,key):
    #     print(key)
    #     if key == "tab":
    #         self.ShowTabMenu()



if __name__ == "__main__":
    app = Ursina()

    ProjectEditor(ExportToPyFunc=Func(print_on_screen,"<color:red>yeah <color:blue>yes"),CurrentTabs=["1","2"],EditorCamera=EditorCamera())
    app.run()
