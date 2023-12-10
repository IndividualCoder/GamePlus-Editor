from GamePlusEditor.ursina import *
import sys
import os
from panda3d.core import WindowProperties

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)

class BlueLink(Button):
    '''Changes mouse to the type like when you hover over a link'''
    def __init__(self, text='...', radius=0.1, ToSubtract=0, Key=None, partKey="", on_key_press=None, on_hover=None, on_unhover=None, hover_highlight=False, hover_highlight_color=color.white, hover_highlight_size=0.2, hover_highlight_button=False, **kwargs) -> None:
        super().__init__(text, radius, ToSubtract, Key, partKey, on_key_press, on_hover, on_unhover, hover_highlight, hover_highlight_color, hover_highlight_size, hover_highlight_button, **kwargs)

        self.MouseCursor: Cursor = Cursor(model = "cube",texture = "../Images/BlueLinkMouse", scale=.033,enabled = False,collider = None,color = color.white)

        self.text_entity.scale: int | float = 2
        self.text_entity.color: color = color.rgb(51,102,204)
        self.color: color = color.red
        self.highlight_color: color  = color.clear
        self.pressed_color: color = color.clear

        self.on_hover: function = self.OnHover
        self.on_unhover: function = self.OnUnhover
        # self.fit_to_text(0,(0,0))
        self.scale: int | float = self.scale


        for key,value in kwargs.items():
            setattr(self,key,value)

    def OnHover(self) -> None:
        '''Makes the cursor hidden and enables the textured cube'''
        self._props = WindowProperties()
        self._props.setCursorHidden(True)
        base.win.requestProperties(self._props)
        self.MouseCursor.enable()

    def OnUnhover(self) -> None:
        '''Makes the cursor visible and disables the textured cube'''
        self._props.setCursorHidden(False)
        base.win.requestProperties(self._props)
        self.MouseCursor.disable()

if __name__ == "__main__":
    app = Ursina()
    a = BlueLink("...",scale = .1)
    window.cursor = 'arrow'
    app.run()