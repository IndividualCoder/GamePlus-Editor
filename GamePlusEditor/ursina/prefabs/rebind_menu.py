from GamePlusEditor.ursina import *

class RebindMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)

        self.bg = Panel(parent=self)

        for key, value in kwargs.items():
            setattr(self, key ,value)


        self.fields = []

        for i, (name, value) in enumerate({'jump':'space', 'left':'d', 'right':'a'}.items()):
            self.fields.append(Button(parent=self, scale=.05, y=.45-(i*.06)))



if __name__ == '__main__':
    app = Ursina()
    RebindMenu()
    app.run()
