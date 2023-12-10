from GamePlusEditor.ursina import *
from GamePlusEditor.GizmoStuff.PositionGizmo import PositionGizmo
from GamePlusEditor.GizmoStuff.ScaleGizmo import ScaleGizmo
from GamePlusEditor.GizmoStuff.RotationGizmo import RotationGizmo

class GizmoManager(Entity):
    def __init__(self):
        self._PositionSnapping = 0
        self._RotationSnapping = 0
        self._ScaleSnapping = 0

        self.OnDrag = None

        self.CurrentGizmo: PositionGizmo | RotationGizmo | ScaleGizmo | None = None

    def AddGizmo(self,Entity,GizmoType: str):
        match GizmoType:
            case "PositionGizmo":
                self.RemoveGizmo()
                self.CurrentGizmo = PositionGizmo(Entity,self.PositionSnapping,OnDrag=self.OnDrag)
                self.CurrentGizmo.SetUp()

            case "RotationGizmo":
                self.RemoveGizmo()
                self.CurrentGizmo = RotationGizmo(Entity,self.RotationSnapping)
                self.CurrentGizmo.SetUp()

            case "ScaleGizmo":
                self.RemoveGizmo()
                self.CurrentGizmo = ScaleGizmo(Entity,self.ScaleSnapping)
                self.CurrentGizmo.SetUp()

    def RemoveGizmo(self):
        if type(self.CurrentGizmo) is not None:
            destroy(self.CurrentGizmo)
            self.CurrentGizmo = None

    def GoToEntity(self):
        if type(self.CurrentGizmo) == None:
            return
        self.CurrentGizmo.GoToEntity()

    @property
    def PositionSnapping(self):
        return self._PositionSnapping
    
    @PositionSnapping.setter
    def PositionSnapping(self,Value: int | float):
        self._PositionSnapping = Value
        if type(self.CurrentGizmo).__name__ == "PositionGizmo":
            self.CurrentGizmo.Snapping = Value

    @property
    def RotationSnapping(self):
        return self._PositionSnapping
    
    @RotationSnapping.setter
    def RotationSnapping(self,Value: int | float):
        self._RotationSnapping = Value
        if type(self.CurrentGizmo).__name__ == "RotationGizmo":
            self.CurrentGizmo.Snapping = Value
    
    @property
    def ScaleSnapping(self):
        return self._PositionSnapping

    @ScaleSnapping.setter
    def ScaleSnapping(self,Value: int | float):
        self._ScaleSnapping = Value
        if type(self.CurrentGizmo).__name__ == "ScaleGizmo":
            self.CurrentGizmo.Snapping = Value

    # @property 
    # def HasGizmo(self):
    #     if type()
            
if __name__ == "__main__":
    GizmoManager()