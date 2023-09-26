from ursina import *
from DirectionBox import PointOfViewSelector as DirectionEntity
# import random
from OtherStuff import TextToVar #,CustomWindow,CurrentFolderNameReturner
from ursina.color import tint
# from panda3d.core import AntialiasAttrib
# import threading
# from panda3d.core import StencilAttrib,CardMaker,ColorWriteAttrib

class SceneEditor(Entity):
    def __init__(self,enabled,SaveFunction,ShowInstructionFunc,EditorCamera,cam2 = camera,CurrentProjectName = "",**kwargs):
        super().__init__(kwargs)

        self.WorldItems = []
        self.Save = SaveFunction
        # self.ToImport  = ToImport
        self.CurrentProjectName = CurrentProjectName
        self.ShowInstructionFunc = ShowInstructionFunc
        self.EditorCamera = EditorCamera
        self.IsEditing = True


        self.AddObjectTextList = ["Add static object","Add dynamic object","Add FPC","Add TPC","Add abstraction"]
        self.AddObjectOnClickFuncList = [self.AddEntityInScene,self.AddEntityInScene,self.AddEntityInScene,self.AddEntityInScene,self.AddEntityInScene]
        self.BasicFunctions = ["Position x: ","Position y: ","Position z: ","Rotation x: ","Rotation y: ","Rotation z: ","Scale x: ","Scale y: ","Scale z: ","Color: ","Texture: "]
        self.ToEditEntity = None
        self.PosSnapping2d = .01
        self.PosSnapping3d = .7

        self.UniversalParentEntity = Entity(parent = cam2.ui,enabled = False)
        self.SideBarTopParentEntity = Entity(parent = self.UniversalParentEntity,model = "cube",enabled = enabled,position = Vec3(-0.68, 0.16, 10),scale = Vec3(0.43, 0.56, 2),color = color.gray)
        self.AddObjectMenuParentEntity = Entity(parent = self.UniversalParentEntity,model = None,enabled = enabled,position = Vec3(0.38, -0.35, 2),scale = Vec3(1.69, 0.1, 1),color = color.dark_gray,origin_y = 1)
        self.SideBarBottomParentEntity = Entity(parent = self.UniversalParentEntity,model = "cube",enabled = enabled,position = Vec3(-0.68, -0.31, -200),scale = Vec3(0.43, 0.38, 2),color = color.tint(color.gray,-.1))
        self.SideBarTopSlideHandler = Button(parent = self.SideBarTopParentEntity,model = "cube",radius=0,visible_self = False,z = -200)


        # self.ToImport.add("from ursina import *")

        # self.SideBarTopSlider = Entity(parent = self.SideBarTopSlideHandler,model = "cube",visible_self = False,z = -202)
        self.ScrollUpdater = self.SideBarTopSlideHandler.add_script(Scrollable(min=-.1,max = .3,scroll_speed = .01))


        self.WorldGrid = [Entity(parent=self, model=Grid(100,100), rotation_x=90, scale=distance(camera.position,(0,0,0)), collider=None, color=color.black33),Entity(parent=self, model=Grid(100,100), rotation_x=90, scale=distance(camera.position,(0,0,0))*10, collider=None, color=color.black33)]
        self.DirectionEntity = DirectionEntity(cam2.ui,window.top_right- Vec2(.1,.038),self.EditorCamera,camera,enabled = enabled,z = -30,always_on_top = True,render_queue = 1)

        self.SpecialEntities = [self.DirectionEntity,self.WorldGrid[0],self.WorldGrid[1]]

    def UpdateScroller(self):
        if len(self.AddObjectMenuParentEntity.children) == 5:
            self.AddedScriptAddObjectMenu.update_target("min",self.AddedScriptAddObjectMenu.min - 0.17)
            return
        self.AddedScriptAddObjectMenu.update_target("min",self.AddedScriptAddObjectMenu.min - 0.3042)

    def GetPosTemp(self):
        self.AddedScriptAddObjectMenu = self.AddObjectMenuParentEntity.add_script(Scrollable(min=.38,max=.38,scroll_speed = .03,axis = "x"))
        for i in range(len(self.AddObjectTextList)):
            self.AddObjectToScroll(Button(parent = self.AddObjectMenuParentEntity,text=self.AddObjectTextList[i],scale = Vec3(0.1800007, 1, 1),radius=0,color=color.blue,texture = "white_cube",position = Vec3(-0.41+i*.18, -1.02, 0),on_click = self.AddObjectOnClickFuncList[i]))
            # print(self.AddedScriptAddObjectMenu.min)

            # self.AddObjectMenuParentEntity.children[i].color = color.white
            # print(self.AddObjectMenuParentEntity.children[i].x,"  :  ",self.AddObjectMenuParentEntity.children[i].name)
        # self.AddObjectMenuParentEntity.add_script(Scrollable(min=len(self.AddObjectMenuParentEntity.children)/-5.2,max=.38,scroll_speed = .03,axis = "x"))

    def AddObjectToScroll(self,object): 
        self.AddObjectMenuParentEntity.children.append(object)
        if len(self.AddObjectMenuParentEntity.children) > 4:
            self.UpdateScroller()

    def AddEntityInScene(self):
        self.WorldItems.append(Entity(name = f"item_{len(self.WorldItems)}",parent = scene,model = "cube",texture = "white_cube",collider = "mesh",collision = True,hovered = True,color = color.white))
        self.ShowObjectContent(self.WorldItems[-1],self.SideBarTopSlideHandler)
        self.ScrollUpdater.update_target("max",34)
        self.ToEditEntity = self.WorldItems[-1]
        self.ToEditEntity.texture._texture.setAnisotropicDegree(128)
    
        # print("helo",type(self.ToEditEntity).__name__)


    def AddFpcInScene(self): print_on_screen(self.AddObjectFpcButton.name)
    def AddTpcInScene(self): print_on_screen(self.AddObjectTpcButton.name)
    def AddAbstractionInScene(self): print_on_screen(self.AddObjectAbstractionButton.name)


        # Vec3(0, 0.5, 0)

    def ShowObjectContent(self,Obj,Parent):
        self.TempLen = len(Parent.children)
        # print(self.TempLen)
        for i in range(self.TempLen-1,-1,-1):
            destroy(Parent.children[i])
        del self.TempLen
        Parent.children = []


        Parent.children.append(Text(parent = Parent,text =type(Obj).__name__,scale = 3,origin = (0,0),y = .45,z = 20,scale_x = 3.5))
        Parent.children.append(Entity(name = "Line",parent = Parent,model = "line",color = color.black,scale = Vec3(0.99, 1.02, 1),position  = Vec3(0.01, 0.39, 20)))

        for i in range(len(self.BasicFunctions)):
            Parent.children.append(Text(parent = Parent,text = f"{self.BasicFunctions[i]}",scale = 2,y = -i*0.08+.36,z = 20,x = -.47))
        
        for i in range(len(self.BasicFunctions)):
            Parent.children.append(InputField(name = TextToVar(self.BasicFunctions[i],'_'),submit_on=["enter","escape"],parent = Parent,default_value = f"{getattr(Obj,TextToVar(self.BasicFunctions[i],'_'))}",y = -i*0.08+.36,z = -20,x = .1,active = False,text_scale = .75,cursor_y = .1,enter_active = True,on_submit = Func(self.UpdateItemContent,Obj,Parent)))

            if i > 0:
                Parent.children[i-1].next_field = Parent.children[i]


    def UpdateItemContent(self,Obj,Parent):
        for i in range((len(Parent.children))):
            if type(Parent.children[i]) == InputField:
                # if not Parent.children[i].name == "color" or not Parent.children[i].name == "texture":
                try:
                    print(Parent.children[i].name ," : ",Parent.children[i].text)

                    setattr(Obj,Parent.children[i].name.replace("position_",""),float(eval(Parent.children[i].text)))

                except:
                    try:
                        self.TempColor:str = Parent.children[i].text.replace("Color(","")
                        self.TempColor  = self.TempColor.replace(")","")

                        self.TempColor = self.TempColor.split(",",maxsplit=3)
                        for i in range(len(self.TempColor)):
                            self.TempColor[i] = float(eval(self.TempColor[i])) * 255
                        print("this: ",self.TempColor)
                        Obj.color = color.rgba(self.TempColor[0],self.TempColor[1],self.TempColor[2],self.TempColor[3])

                    except Exception as e:
                        print(e)
                # print(f"  :  {Parent.children[i].name}  :  {Parent.children[i].text}")

        # print(Parent.children)

    def input(self,key):
        # print(key)
        if self.IsEditing:
            if key == "s" and held_keys["control"] and not held_keys["shift"]:
                self.SaveEditor()

            elif key in ["left mouse","left mouse down"]:
                if mouse.hovered_entity in self.WorldItems:
                    if mouse.hovered_entity == self.ToEditEntity:
                        return

                    self.ToEditEntity =  mouse.hovered_entity
                    self.ShowObjectContent(self.ToEditEntity,self.SideBarTopSlideHandler)

            elif key in ["right arrow","right arrow hold"]:
                try:
                    # if self.ToEditEntity.parent:
                    self.ToEditEntity.x += self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                    # else:
                    #     self.ToEditEntity.x += self.PosSnapping3d
                        # print(mouse.hovered_entity.name)

                except AttributeError:
                    print_on_screen("<red>Choose an item to edit")
            elif key in ["left arrow","left arrow hold"]:
                try:

                    # if self.ToEditEntity.parent:
                    self.ToEditEntity.x -= self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                    # else:
                    #     self.ToEditEntity.x += self.PosSnapping3d
                except AttributeError:
                    print_on_screen("hoose an item to edit",color = color.red)
            elif key in ["up arrow","up arrow hold"]:
                try:
                    # if self.ToEditEntity.parent:
                    self.ToEditEntity.y += self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                    # else:
                    #     self.ToEditEntity.x += self.PosSnapping3d
                except AttributeError:
                    print_on_screen("Choose an item to edit",origin=0,color = color.orange)
            elif key in ["down arrow","down arrow hold"]:
                try:

                    # if self.ToEditEntity.parent:
                    self.ToEditEntity.y -= self.PosSnapping2d
                    # print(mouse.hovered_entity.name)
                    # else:
                    #     self.ToEditEntity.x += self.PosSnapping3d
                except AttributeError:
                    print_on_screen("<red>Choose an item to edit")

            elif key == "right mouse up" and mouse.hovered_entity in self.WorldItems:
                # if mouse.hovered_entity in self.WorldItems:
                    # mouse.hovered_entity
                    self.ToEditEntity = mouse.hovered_entity
                    # print(self.ToEditEntity)

            elif key == "delete up":
                try:
                    index = self.WorldItems.index(self.ToEditEntity)
                    destroy(self.ToEditEntity)
                    del self.WorldItems[index]
                    self.ToEditEntity = None
                except ValueError:
                    pass


    def update(self):
        if self.IsEditing:
            self.WorldGrid[0].scale=distance(camera.position,(0,0,0)) - .4
        
    def MakeEditorEnvironment(self,cam,color,size):

        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0]/255,color[1]/255,color[2]/255,color[3]/255)
        # print(size)

    def DisableEverything(self):
        # self.UniversalParentEntity.disable()
        self.EditorCamera.disable()
        self.IsEditing = False

    def EnableEverything(self,Entity):
        # Entity.enable()
        # for i in range(len(Entity.children)):
        #     Entity.children[i].enable()
        #     if len(Entity.children[i].children) > 0:
        #         self.EnableEverything(Entity.children[i])
        self.EditorCamera.enable()

        self.IsEditing = True

    def Setup(self):
        self.DirectionEntity.front_text.render_queue = 1
        self.DirectionEntity.back_text.render_queue = 1
        self.DirectionEntity.left_text.render_queue = 1
        self.DirectionEntity.right_text.render_queue = 1
        self.DirectionEntity.top_text.render_queue = 1
        self.DirectionEntity.bottom_text.render_queue = 1

    def SaveEditor(self):
        self.Save()
        self.ShowInstructionFunc("Your project is saved :)",Color = tint(color.white,-.6),Title = "Saved!")

if __name__ == "__main__":
    from OtherStuff import *
    # from ursina.camera import Camera
    app = Ursina()
    # window.fullscreen = True
    # dr = application.base.camNode.getDisplayRegion(0)
    from ursina.prefabs.memory_counter import MemoryCounter
    MemoryCounter()
    # dr.setDimensions(0.2399, .999, 0.1009, 0.938)
    # print(scene.entities)
    window.fps_counter.disable()
    window.exit_button.disable()
    # cam2 = Camera()

    editor = EditorCamera()
    scene_editor = SceneEditor(editor_camera=editor,enabled=True,WorldItems=[],ToImport=set(),EditorCamera=editor,SaveFunction=Func(print,"hele"),ShowInstructionFunc=Func(print,"hele"))
    scene_editor.UniversalParentEntity.enabled = True
    scene_editor.GetPosTemp()
    Sky()

    # camera.ui_display_region.setDimensions(0./2399, .999, 0.1009, 0.938)
    # ui_dr.setDimensions(0.2399, .999, 0.1009, 0.938)
    # print(window.screen_resolution)
    print(application.base.camNode.getDisplayRegion(0))
    '''0.2399, .999, 0.1009, 0.938'''
    # scene_editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, 1, 0.1009, 0.938))

    def input(key):
        if key == "l":
            for i in range(len(camera.ui.children)):
                camera.ui.children[i].enabled = not camera.ui.children[i].enabled
        if key == "q":
            application.quit()
    app.run()

