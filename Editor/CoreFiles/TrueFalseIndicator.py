from ursina import *
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)
from OtherStuff import MultiFunctionCaller

class TrueFalseIndicator(Entity):
    def __init__(self,DefaultState,StateList,OnClick = None,**kwargs):
        super().__init__(parent = kwargs["parent"])
        self.position = kwargs["position"]
        self.scale = kwargs["scale"]
        if OnClick is not None:
            self.Button = Button(parent = self,text=DefaultState,on_click = Func(MultiFunctionCaller,self.ChangeState,OnClick),font = "VeraMono.ttf")
        else:
            self.Button = Button(parent = self,text=DefaultState,on_click = Func(MultiFunctionCaller,self.ChangeState),font = "VeraMono.ttf")

        self.StateList = StateList
        self.Button.text_entity.scale += (.05,.3,.3)
        self.Button.text_entity.position = (-.5+.05,0)
        self.Button.text_entity.origin = (-.5,0)

    def ChangeState(self):
        for i in range(len(self.StateList)):
            if self.StateList[i] == self.Button.text:
                if i < len(self.StateList) - 1:
                    self.Button.text = self.StateList[i + 1]
                    break
                else:
                    self.Button.text = self.StateList[0]  # Wrap around to the first element
                    break

        self.Button.text_entity.scale += (.05,.3,.3)
        self.Button.text_entity.position = (-.5+.05,0)
        self.Button.text_entity.origin = (-.5,0)
        # if self.StateList[0] == self.Button.text:
        #     self.Button.text = self.StateList[1]
        # else:
        #     self.Button.text = self.StateList[0]
        # for i in range(len(self.StateList)):
        #     if self.StateList[i] == self.CurrentState:
        #         self.CurrentState = self.StateList[i+1]

if __name__ == "__main__":
    app = Ursina()
    b = TrueFalseIndicator('1',['1','2',"3"],OnClick=Func(print,"hi"),position = Vec3(0.2, 0.37-0*0.07, -10),scale = Vec3(0.32, 0.05, 1),parent = camera.ui)
    def input(key):
        print(b.Button.text)
    app.run()