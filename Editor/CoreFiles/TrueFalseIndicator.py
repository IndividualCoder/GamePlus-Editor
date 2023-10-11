from ursina import *
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)
from OtherStuff import MultiFunctionCaller

class TrueFalseIndicator(Entity):
    """Not really a true false indicator but a button you can click and its text will change as given.\n
      The idea was to limit it just to true and false but you can add as many StateList items as you want.\n
      First argument DefaultState will be the default text of the button."""

    def __init__(self,DefaultState,StateList,OnClick = None,**kwargs):
        super().__init__(parent = kwargs["parent"])
        self.position = kwargs["position"]
        self.scale = kwargs["scale"]
        if OnClick is not None:
            self.Button = Button(parent = self,text=DefaultState,on_click = Func(MultiFunctionCaller,self.ChangeState,OnClick),font = "VeraMono.ttf")
        else:
            self.Button = Button(parent = self,text=DefaultState,on_click = Func(MultiFunctionCaller,self.ChangeState),font = "VeraMono.ttf")

        self.Button.text_entity.scale += (.05,.3,.3)
        self.Button.text_entity.position = (-.5+.05,0)
        self.Button.text_entity.origin = (-.5,0)

        self.StateGenertor = self.GeneratorOfText(StateList)

    def GeneratorOfText(self,List):
        while True:
            yield from List

    def ChangeState(self):
        self.ButtonOrgScale = self.Button.text_entity.scale
        self.Button.text = next(self.StateGenertor)
        self.Button.text_entity.scale = self.ButtonOrgScale
        del self.ButtonOrgScale        

if __name__ == "__main__":
    app = Ursina()
    b = TrueFalseIndicator('1',['hello','hihihihih',"bye"],OnClick=Func(print,"hi"),position = Vec3(0.2, 0.37-0*0.07, -10),scale = Vec3(0.32, 0.05, 1),parent = camera.ui)

    app.run()

