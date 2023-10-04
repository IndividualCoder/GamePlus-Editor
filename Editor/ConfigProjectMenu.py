from ursina import *
import json
import os
from OtherStuff import MultiFunctionCaller

class ConfigProjectManager(Entity):
    '''Not done yet ;)'''
    def __init__(self,Parent,Path,CancelClick,SaveClick):
        super().__init__(parent = Parent)
        self.ProjectPath = Path

        self.UniversalParentEntity = Entity(parent = self)
        self.BackGround = Entity(parent = self.UniversalParentEntity,model = "cube",scale = 10,color = color.black66)
        
        self.CancelButton = Button(parent = self.UniversalParentEntity,name = "cancel button",text = "Cancel",position = Vec3(-0.74, 0.42, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.13, 1),on_click = CancelClick)
        self.SaveButton = Button(parent = self.UniversalParentEntity,name = "save buton",text = "Save and exit",position = Vec3(-0.46, 0.42, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.130001, 1),on_click = Func(MultiFunctionCaller,SaveClick,CancelClick))



        Button(scale = (.001,.001),Key=["w","w hold"],on_key_press=Func(self.SetPos,self.CancelButton,"y",.01))
        Button(scale = (.001,.001),Key=["s","s hold"],on_key_press=Func(self.SetPos,self.CancelButton,"y",-.01))
        Button(scale = (.001,.001),Key=["a","a hold"],on_key_press=Func(self.SetPos,self.CancelButton,"x",-.01))
        Button(scale = (.001,.001),Key=["d","d hold"],on_key_press=Func(self.SetPos,self.CancelButton,"x",.01))

        Button(scale = (.001,.001),Key=["up arrow","up arrow hold"],on_key_press=Func(self.SetPos,self.SaveButton,"y",.01))
        Button(scale = (.001,.001),Key=["down arrow","down arrow hold"],on_key_press=Func(self.SetPos,self.SaveButton,"y",-.01))
        Button(scale = (.001,.001),Key=["left arrow","left arrow hold"],on_key_press=Func(self.SetPos,self.SaveButton,"x",-.01))
        Button(scale = (.001,.001),Key=["right arrow","right arrow hold"],on_key_press=Func(self.SetPos,self.SaveButton,"x",.01))

        Button(scale = (.001,.001),Key=["1","1 hold"],on_key_press=Func(self.SetPos,self.CancelButton,"scale_x",.01))
        Button(scale = (.001,.001),Key=["2","2 hold"],on_key_press=Func(self.SetPos,self.CancelButton,"scale_x",-.01))
        Button(scale = (.001,.001),Key=["3","3 hold"],on_key_press=Func(self.SetPos,self.CancelButton,"scale_y",.01))
        Button(scale = (.001,.001),Key=["4","4 hold"],on_key_press=Func(self.SetPos,self.CancelButton,"scale_y",-.01))

        Button(scale = (.001,.001),Key=["5","5 hold"],on_key_press=Func(self.SetPos,self.SaveButton,"scale_x",.01))
        Button(scale = (.001,.001),Key=["6","6 hold"],on_key_press=Func(self.SetPos,self.SaveButton,"scale_x",-.01))
        Button(scale = (.001,.001),Key=["7","7 hold"],on_key_press=Func(self.SetPos,self.SaveButton,"scale_y",.01))
        Button(scale = (.001,.001),Key=["8","8 hold"],on_key_press=Func(self.SetPos,self.SaveButton,"scale_y",-.01))
    
        Button(scale = (.001,.001),Key="p",on_key_press=Func(self.ShowPos,self.UniversalParentEntity))
    
        Button(scale = (.001,.001),Key="o",on_key_press=Func(self.SetPos,self.CancelButton,"text",""))
        Button(scale = (.001,.001),Key="o",on_key_press=Func(self.SetPos,self.SaveButton,"text",""))



    def ShowPos(self,item):
        for i in range(len(item.children)):
            print(f'Name: {item.children[i].name} , position = {item.children[i].position} , rotation = {item.children[i].rotation} , scale = {item.children[i].scale}')
            if item.children[i].children != []:
                self.ShowPos(item.children[i])


    def SetPos(self,Entity,Axis,Val):
        setattr(Entity,Axis,getattr(Entity,Axis) + Val)

    def Show(self,Name):
        with open(f"{self.ProjectPath}/{Name}/Game settings.txt","r")  as File:
            self.GameSettings = json.load(File)

        for i,j in enumerate(self.GameSettings):
            print(i,j)



if __name__ == "__main__":
    from OtherStuff import CurrentFolderNameReturner
    app = Ursina()
    pro = ConfigProjectManager(Entity(parent = camera.ui),CurrentFolderNameReturner().replace("Editor","Current games"),Func(print,"hi"),Func(print,"helo")).Show("a")
    app.run()