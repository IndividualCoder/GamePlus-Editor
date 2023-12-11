import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)

from GamePlusEditor.ursina import *
from GamePlusEditor.OtherStuff import CurrentFolderNameReturner,RecursivePerformer
from GamePlusEditor.CoreFiles.TrueFalseIndicator import TrueFalseIndicator


class JoinProjectMenu(Entity):
    '''A simple Ui to let the user join a project\nJoining will only work locally'''
    def __init__(self,CancelClick,ToDoOnInit):
        super().__init__(parent = camera.ui)
        self.CancelClick = CancelClick


        self.UniversalParentEntity = Entity(parent = self)
        self.BackGround = Entity(parent = self.UniversalParentEntity,model = "cube",scale = 10,color = color.black66)

        self.IpInputField = InputField(name = "ip",parent = self.UniversalParentEntity,character_limit=20,placeholder="Enter the ip of the server",position = Vec3(-0.02, 0.13, 0) ,scale = Vec3(0.7, 0.06, 1),active  = False)
        self.PortInputField = InputField(name = "port",parent = self.UniversalParentEntity,character_limit=20,placeholder="Enter the port of the server",limit_content_to = "1234567890",position = Vec3(-0.02, -0.03, 0)  , rotation = Vec3(0, 0, 0) , scale = Vec3(0.7, 0.06, 1),active  = False)

        self.BakcButton = Button(name = "back",parent = self.UniversalParentEntity,text="Back",Key="escape",position = Vec3(-0.234999, -0.28, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.130001, 1),on_click  = self.Close)
        self.JoinButton = Button(name = "join",parent = self.UniversalParentEntity,text = "Join", position = Vec3(0.19, -0.28, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.130001, 1))

        ToDoOnInit()
    # def ShowPos(self,item):
    #     for i in range(len(item.children)):
    #         print(f'Name: {item.children[i].name} , position = {item.children[i].position} , rotation = {item.children[i].rotation} , scale = {item.children[i].scale}')
    #         if item.children[i].children != []:
    #             self.ShowPos(item.children[i])


    # def SetPos(self,Entity,Axis,Val):
    #     setattr(Entity,Axis,getattr(Entity,Axis) + Val)

    # def Retext(self):
    #     for i in range(len(self.UniversalParentEntity.children)):
    #         if type(self.UniversalParentEntity.children[i])  in [Button,InputField]:
    #             self.UniversalParentEntity.children[i].text = self.UniversalParentEntity.children[i].text

    def Close(self) -> None:
        '''Closes the menu'''
        RecursivePerformer(self.UniversalParentEntity,destroy,BasicFunc=False)
        destroy(self)
        self.CancelClick()

if __name__ == "__main__":
    from GamePlusEditor.OtherStuff import CurrentFolderNameReturner
    app = Ursina()
    pro = JoinProjectMenu(Entity(parent = camera.ui),f"{CurrentFolderNameReturner()}/Current Games",Func(print,"hi"))
    Sky()
    app.run()