from GamePlusEditor.ursina import *

class BaseGizmoClass(Entity):
    def __init__(self,OnDragged,Entity,Snapping,DraggingProperty: str,**kwargs):
        super().__init__()
        self.Entity = Entity
        self.OnDragged: function = OnDragged

        self.GizmoX = Draggable(parent = self,lock = (0,1,1),model = 'cube',scale = (2,.2,.2),color = color.red)
        self.GizmoY = Draggable(parent = self,lock = (1,0,1),model = 'cube',scale = (.2,2,.2),color = color.blue)
        self.GizmoZ = Draggable(parent = self,lock = (1,0,0),plane_direction = (0,1,0),model = 'cube',scale = (.2,.2,2),color = color.green)

        self.CurrentlyDragging: Draggable = self.GizmoX
        for attribute,value in kwargs.items():
            setattr(self,attribute,value)

    def update(self):
        self.Entity.position = self.CurrentlyDragging.position
        self.GizmoX.position = self.CurrentlyDragging.position
        self.GizmoY.position = self.CurrentlyDragging.position
        self.GizmoZ.position = self.CurrentlyDragging.position

    def SetUp(self):
        self.GizmoX.drag = lambda: setattr(self,"CurrentlyDragging" ,self.GizmoX)
        self.GizmoY.drag = lambda: setattr(self,"CurrentlyDragging" ,self.GizmoY)
        self.GizmoZ.drag = lambda: setattr(self,"CurrentlyDragging" ,self.GizmoZ)

if __name__ == "__main__":
    app = Ursina()
    a = Entity(model = "cube")
    BaseGizmoClass(...,a,.2,"position").SetUp()
    EditorCamera()
    app.run()