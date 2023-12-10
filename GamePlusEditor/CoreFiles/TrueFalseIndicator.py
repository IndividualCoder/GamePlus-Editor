from GamePlusEditor.ursina import *
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)
from GamePlusEditor.OtherStuff import MultiFunctionCaller

class TrueFalseIndicator(Entity):
    '''Not really a true false indicator but a button you can click and its text will change as given.\n
      The idea was to limit it just to true and false but you can add as many StateList items as you want.\n
      First argument DefaultState will be the default text of the button.'''

    def __init__(self,StateList,OnClick = None,DefaultState = "",**kwargs) -> None: #Doesn't matter if you give DefaultState or not, it will be ignored
        super().__init__()

        if OnClick is not None:
            self.Button: Button = Button(parent = self,text=DefaultState,on_click = Func(MultiFunctionCaller,self.ChangeState,OnClick),font = "VeraMono.ttf")
        else:
            self.Button: Button = Button(parent = self,text=DefaultState,on_click = self.ChangeState,font = "VeraMono.ttf")


        self.StateGenertor: function = self.GeneratorOfText(StateList)
        self.ChangeState() # get the default state

        if DefaultState != "":
            self.Button.text = DefaultState
        for key, value in kwargs.items():
            setattr(self,key,value)
        self.Button.text_entity.origin: Vec3 = (-.5,0)
        self.Button.text_entity.position: Vec3 = (-.48,0,0)
        self.Button.text_entity.scale: Vec3 =  self.Button.text_entity.scale + (-.7,.3,.3)

    def GeneratorOfText(self,List: list):
        '''A generator to return the next item form the StateList\nReturns first item form the list if current state is last elemnt of the list'''
        while True:
            yield from List

    def ChangeState(self) -> None:
        '''Changes the text to the next text of the StateList'''
        self.ButtonOrgScale: Vec3 = self.Button.text_entity.scale
        self.Button.text: str = next(self.StateGenertor)
        # print(self.Button.text)
        self.Button.text_entity.scale: Vec3 = self.ButtonOrgScale
        del self.ButtonOrgScale        

if __name__ == "__main__":
    app = Ursina()
    b = TrueFalseIndicator(['hello','hihihihih',"bye"],OnClick=Func(print,"hi"),position = Vec3(0.2, 0.37-0*0.07, -10),scale = Vec3(0.32, 0.05, 1),parent = camera.ui)

    app.run()

