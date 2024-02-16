from GamePlusEditor.ursina import *
from GamePlusEditor.GizmoStuff.PositionGizmo import PositionGizmo
from GamePlusEditor.GizmoStuff.ScaleGizmo import ScaleGizmo
from GamePlusEditor.GizmoStuff.RotationGizmo import RotationGizmo

class GizmoManager(Entity):
    '''Manages all the gizmo stuff for the scene editor'''
    def __init__(self): 
        super().__init__()
        self._PositionSnapping:float | int = 0
        self._RotationSnapping:float | int = 0
        self._ScaleSnapping:float | int = 0

        self.OnDrag = None
        self.CurrentGizmoEntity: Entity = None

        self.CurrentGizmo: PositionGizmo | RotationGizmo | ScaleGizmo | None = None

    def AddGizmo(self,Entity,GizmoType: str,OnGizmoAdded = None):
        '''Makes the gizmo for the given entity'''
        match GizmoType:
            case "PositionGizmo":
                self.RemoveGizmo() #Remove the last gizmo
                self.CurrentGizmo = PositionGizmo(Entity,Snapping=self.PositionSnapping,OnDrag=self.OnDrag,parent = self)
                self.CurrentGizmo.SetUp()

            case "RotationGizmo":
                self.RemoveGizmo()
                self.CurrentGizmo = RotationGizmo(Entity,Snapping=self.RotationSnapping,OnDrag=self.OnDrag,parent = self)
                self.CurrentGizmo.SetUp()

            case "ScaleGizmo":
                self.RemoveGizmo()
                self.CurrentGizmo = ScaleGizmo(Entity,Snapping=self.ScaleSnapping,OnDrag=self.OnDrag,parent = self)
                self.CurrentGizmo.SetUp()

        self.CurrentGizmoEntity = Entity

        if OnGizmoAdded != None:
            OnGizmoAdded()

    def RemoveGizmo(self):
        '''Removes the current gizmo only if it is not "None"'''
        if type(self.CurrentGizmo) is not None:
            destroy(self.CurrentGizmo)
            self.CurrentGizmo = None

    def GoToEntity(self):
        '''Chanes the position of current gizmo to the position of the entity'''
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