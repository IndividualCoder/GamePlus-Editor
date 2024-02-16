from GamePlusEditor.ursina import *
from GamePlusEditor.CoreFiles.BlueLink import BlueLink
from GamePlusEditor.OtherStuff import MultiFunctionCaller,RecursivePerformer

class ColorMenu(Button):
    '''Choose color by sliding sliders instead of putting random int'''
    def __init__(self,EntityToColor,BGScale,BGPos = (0,0,0),WordLimit = 20,**kwargs):
        super().__init__()
        self.WordLimit = WordLimit
        self.EntityToColor = EntityToColor

        for key,value in kwargs.items():
            setattr(self,key,value)

        self.UniversalParnetEntity = Entity(enabled = self.enabled,parent =camera.ui,model = "cube",collider = None,visible_self = False,world_position = self.world_position)
        self.UniversalParnetEntity.world_scale = self.world_scale
        

        self.ColorMenuBG = Entity(model = "cube",parent = self.UniversalParnetEntity,color = color.tint(color.gray,-0.4),z = -9,enabled = False,position = BGPos,collider = "mesh",scale = BGScale,always_on_top = True)

        self.EntityNameText = Text(parent = self.ColorMenuBG,position =  Vec3(-0.49, 0.49, -2),rotation = Vec3(0, 0, 0),scale = Vec3(2, 2, 1))


        self.SliderR = Slider(name = "slider r",parent = self.ColorMenuBG,min  = 0,max=255,default=self.EntityToColor.color[0]*255,dynamic=True,text="Red",position =  Vec3(-0.3, 0.35, -2),rotation = Vec3(0, 0, 0),scale = Vec3(1.5, 1.5, 1.5),on_value_changed = self.UpdatePreview)
        self.SliderG = Slider(name = "slider g",parent = self.ColorMenuBG,min  = 0,max=255,default=self.EntityToColor.color[1]*255,dynamic=True,text="Green",position =  Vec3(-0.3, 0.26, -2),rotation = Vec3(0, 0, 0),scale = Vec3(1.5, 1.5, 1.5),on_value_changed = self.UpdatePreview)
        self.SliderB = Slider(name = "slider b",parent = self.ColorMenuBG,min  = 0,max=255,default=self.EntityToColor.color[2]*255,dynamic=True,text="Blue",position =  Vec3(-0.3, 0.17, -2),rotation = Vec3(0, 0, 0),scale = Vec3(1.5, 1.5, 1.5),on_value_changed = self.UpdatePreview)
        self.SliderA = Slider(name = "slider a",parent = self.ColorMenuBG,min  = 0,max=255,default=self.EntityToColor.color[3]*255,dynamic=True,text="Alpha",position =  Vec3(-0.3, 0.08, -2),rotation = Vec3(0, 0, 0),scale = Vec3(1.5, 1.5, 1.5),on_value_changed = self.UpdatePreview)

        self.ColorPreviewText = Text(parent = self.ColorMenuBG,text= "Preview: ",position = (-.48,-.02,-2),scale = 1.5)
        self.ColorPreviewEntity = Entity(parent = self.ColorMenuBG,model = 'cube',scale = (.3,.2),position = (-.16,-.06,-2))

        self.CancelColorButton = Button(name = "cancel button",parent = self.ColorMenuBG,color = color.tint(color.blue),text="Cancel",  position =  Vec3(-0.25, -0.33, -2),rotation = Vec3(0, 0, 0),scale = Vec3(0.420001, 0.220001, 1),on_click = self.CancelColor)
        self.SaveColorButton = Button(name = "save button",parent = self.ColorMenuBG,color = color.tint(color.blue),text="Save", position =  Vec3(0.25, -0.33, -2),rotation = Vec3(0, 0, 0),scale = Vec3(0.420001, 0.220001, 1),on_click = self.SaveColor)

        self.CloseColorMenuButton = Button(name = "Close Button",parent = self.ColorMenuBG,position =  Vec3(0.47, 0.47, -10),rotation = Vec3(0, 0, 0),scale = Vec3(0.045, 0.045, 1),text="X",color = color.clear,on_click = self.CancelColorButton.on_click)
        self.CloseColorMenuButton.text_entity.scale = 2


    def on_click(self):
        RecursivePerformer(self.UniversalParnetEntity,"enable")



    def DisableColorMenu(self):
        self.ColorMenuBG.disable()

    def ExtractName(self):
        return "color"
    
    def ExtractData(self,OwnSelf):
        return color.rgba(self.SliderR.value,self.SliderG.value,self.SliderB.value,self.SliderA.value)

    def UpdatePreview(self):
        self.ColorPreviewEntity.color = color.rgba(self.SliderR.value,self.SliderG.value,self.SliderB.value,self.SliderA.value)

    def SetUp(self):
        if len(self.EntityToColor.name) > self.WordLimit:
            self.EntityNameText.text = self.EntityToColor.name[0: self.WordLimit-3]
            self.BlueLinkButton  =BlueLink(parent = self.EntityNameText,on_click = Func(setattr,self.EntityNameText,"text",self.EntityToColor.name),scale = .1,x = self.EntityNameText.width,z = self.EntityNameText.z)
            self.BlueLinkButton.x += .05

        else:
            self.EntityNameText.text = self.EntityToColor.name

        self.SaveColorButton.text = self.SaveColorButton.text
        self.CancelColorButton.text = self.CancelColorButton.text


        self.SliderR._update_text()
        self.SliderG._update_text()
        self.SliderB._update_text()
        self.SliderA._update_text()

        self.UpdatePreview()
        self.color = self.ColorPreviewEntity.color

    def SaveColor(self):
        self.EntityToColor.color = self.ColorPreviewEntity.color
        self.color = self.ColorPreviewEntity.color
        self.DisableColorMenu()

    def CancelColor(self):
        self.ColorPreviewEntity.color = self.EntityToColor.color
        self.SliderR.value = self.EntityToColor.color[0] * 255
        self.SliderG.value = self.EntityToColor.color[1] * 255
        self.SliderB.value = self.EntityToColor.color[2] * 255
        self.SliderA.value = self.EntityToColor.color[3] * 255
        self.DisableColorMenu()


if __name__ == "__main__":
    app  = Ursina()
    a = ColorMenu(Button(name = "ladsfjkladlkjhgfdfghjkkjhgs",parent = scene,color = color.red),(.9,.9))
    # a.scale = (.2,.2)
    # a.color = color.white

    a.SetUp()
    EditorCamera()
    app.run()



