import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)

from GamePlusEditor.ursina import *

from GamePlusEditor.OtherStuff import MultiFunctionCaller,RecursivePerformer,CustomWindow



class HostProjectMenu(Entity):
    '''A simple window panel to let the user host its project\nJoining will only work locally'''
    def __init__(self,CancelClick,ToDoOnInit,Ip,Port,ToDoOnHost,Queue = 0,**kwargs):
        super().__init__(parent = camera.ui)
        self.CancelClick = CancelClick


        self.UniversalParentEntity = Entity(parent = self,render_queue = Queue)


        self.Window = CustomWindow(self.Close,title="Host project",OnEnable=None,content=[Text("Send the port and ip to the client."),Text(f"The ip is: {Ip}"),Text(f"The port is: {Port}"),Button(name = "back",parent = self.UniversalParentEntity,text="Cancel",Key="escape",position = Vec3(-0.234999, -0.28, -204) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.130001, 1),on_click  = self.Close),Button(name = "join",parent = self.UniversalParentEntity,text = "Host", position = Vec3(0.19, -0.28, -204) , rotation = Vec3(0, 0, 0),Key = "enter" ,on_click = Func(MultiFunctionCaller,ToDoOnHost,self.Close), scale = Vec3(0.270001, 0.130001, 1))])
        self.Window.WindowPanelOfQuit.text_entity.z = -204
        self.Window.WindowPanelOfQuit.text_entity.render_queue = 3

        if  ToDoOnInit is not None:
            ToDoOnInit()

    def Close(self):
        RecursivePerformer(self.UniversalParentEntity,destroy,BasicFunc=False)
        destroy(self)
        RecursivePerformer(self.Window.QuitMenuParentEntity,destroy,BasicFunc=False)

        if self.CancelClick is not None:
            self.CancelClick()



if __name__ == "__main__":
    from GamePlusEditor.OtherStuff import CurrentFolderNameReturner
    app = Ursina()
    pro = HostProjectMenu(Entity(parent = camera.ui),Func(print,"hi"),"localhost",100,Func(print,"Hi"))
    Sky()
    app.run()