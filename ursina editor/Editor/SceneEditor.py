from ursina import *
from DirectionBox import PointOfViewSelector as DirectionEntity
# import random
from OtherStuff import TextToVar

class SceneEditor(Entity):
    def __init__(self,editor_camera,enabled,WorldItems: list,cam2 = camera,**kwargs):
        super().__init__(enabled = enabled,**kwargs)
        # self.Path = Path
        self.WorldItems = WorldItems

        self.BasicFunctions = ["Position x: ","Position y: ","Position z: ","Rotation x: ","Rotation y: ","Rotation z: ","Scale x: ","Scale y: ","Scale z: ","Color: ","Texture: "]
        self.ToEditEntity = None
        self.PosSnapping2d = .01
        self.PosSnapping3d = .7

        self.UniversalParentEntity = Entity(parent = cam2.ui,enabled = False)
        self.TopButtonsParentEntity = Entity(parent = self.UniversalParentEntity,enabled = enabled,model = "cube",color = color.white.tint(-3),texture ="white_cube",position  = (window.top[0],window.top[1] - .03,-3) ,scale =(window.screen_resolution[0] / 1052,window.screen_resolution[1]/18000))
        self.TabsMenuParentEntity = Button(parent  = self.UniversalParentEntity,enabled = enabled,model = "cube",color = color.green,position  = Vec3(0, 0.5, -1) ,scale = Vec3(1.78, 0.1, 1),Key = "tab",on_key_press=self.ShowTabMenu) # Vec3(0, 0.39, 1) animate
        self.SideBarTopParentEntity = Entity(name = "TODO",parent = self.UniversalParentEntity,model = "cube",enabled = enabled,position = Vec3(-0.68, 0.16, 1),scale = Vec3(0.43, 0.56, 2),color = color.gray)
        self.AddObjectMenuParentEntity = Entity(name = "a;lld",parent = self.UniversalParentEntity,model = None,enabled = enabled,position = Vec3(0.38, -0.35, 2),scale = Vec3(1.69, 0.1, 1),color = color.dark_gray,origin_y = 1)
        self.SideBarBottomParentEntity = Entity(name = "TODO2",parent = self.UniversalParentEntity,model = "cube",enabled = enabled,position = Vec3(-0.68, -0.31, -200),scale = Vec3(0.43, 0.38, 2),color = color.tint(color.gray,-.1))
        self.SideBarTopSlideHandler = Entity(parent = self.SideBarTopParentEntity,model = "cube",visible_self = False,z = -200)
        self.SideBarTopSlider = Entity(parent = self.SideBarTopSlideHandler,model = "cube",visible_self = False,z = -202)
        self.ScrollUpdater = self.SideBarTopSlideHandler.add_script(Scrollable(min=-.1,max = .3,scroll_speed = .01))


        self.WorldGrid = [Entity(parent=self, model=Grid(100,100), rotation_x=90, scale=distance(camera.position,(0,0,0)), collider='box', color=color.black33),Entity(parent=self, model=Grid(100,100), rotation_x=90, scale=distance(camera.position,(0,0,0))*10, collider='box', color=color.black33)]
        self.SaveProjectButton = Button(parent = self.TopButtonsParentEntity,text="Save",color = color.blue,radius  = 0,position =(-0.437, 0, -1),scale = (1/11,0.7)) #Vec3(0.179, 0.0385, 1)
        self.FinishProjectButton = Button(parent = self.TopButtonsParentEntity,text="Finish",color = color.blue,radius  = 0,position =(-0.337, 0, -1),scale = (1/11,0.7)) #Vec3(0.179, 0.0385, 1)
        self.PlayProjectButton = Button(parent = self.TopButtonsParentEntity,text="Play",color = color.blue,radius  = 0,position =(-0.237, 0, -1),scale = (1/11,0.7)) #Vec3(0.179, 0.0385, 1)
        self.DirectionEntity = DirectionEntity(cam2.ui,window.top_right- Vec2(.1,.038),editor_camera,camera,enabled = enabled,z = -30)

        #will make these buttons generate by a function later in time
        self.AddObjectEntityButton = Button(name = "Add an entity in scene",parent = self.AddObjectMenuParentEntity,text="Add Entity",texture = "white_cube",position = Vec3(-0.41, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddEntityInScene)
        self.AddObjectButtonButton = Button(name = "Add a button in scene",parent = self.AddObjectMenuParentEntity,text="Add Button",texture = "white_cube",position = Vec3(-0.23, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddButtonInScene)
        self.AddObjectCharacterButton = Button(name = "Add a button in scene",parent = self.AddObjectMenuParentEntity,text="Add an\nAI character",texture = "white_cube",position = Vec3(-0.05, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddButtonInScene)
        self.AddObjectInputFieldButton = Button(name = "Add a input field in scene",parent = self.AddObjectMenuParentEntity,text="Add Input field",texture = "white_cube",position = Vec3(0.13, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddInputFieldInScene)
        self.AddObjectTextFieldButton = Button(name = "Add a text field in scene",parent = self.AddObjectMenuParentEntity,text="Add Text field",texture = "white_cube",position = Vec3(0.31, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddTextFieldInScene)
        self.AddObjectDraggableButton = Button(name = "Add a draggable in scene",parent = self.AddObjectMenuParentEntity,text="Add Draggable",texture = "white_cube",position = Vec3(0.49, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddDraggableInScene)
        self.AddObjectDropdownSimpleButton = Button(name = "Add a dropdown(simple) in scene",parent = self.AddObjectMenuParentEntity,text="Add\nSimple Dropdown",texture = "white_cube",position = Vec3(0.67, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddDropdownSimpleInScene)
        self.AddObjectDropdownAdvanceButton = Button(name = "Add a dropdown(advance) in scene",parent = self.AddObjectMenuParentEntity,text="Add\nAdvance Dropdown",texture = "white_cube",position = Vec3(0.85, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddDropdownAdvanceInScene)
        self.AddObjectCustomWindowButton = Button(name = "Add a custom window in scene",parent = self.AddObjectMenuParentEntity,text="Add Window panel",texture = "white_cube",position = Vec3(1.02, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddCustomWindowInScene)
        self.AddObjectHealthbarButton = Button(name = "Add a healthbar in scene",parent = self.AddObjectMenuParentEntity,text="Add Healthbar",texture = "white_cube",position = Vec3(1.2, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddHealthbarInScene)
        self.AddObjectSliderButton = Button(name = "Add a slider in scene",parent = self.AddObjectMenuParentEntity,text="Add Horizontal Slider",texture = "white_cube",position = Vec3(1.3899, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddSliderInScene)
        self.AddObjectThinSliderButton = Button(name = "Add a vertical slider in scene",parent = self.AddObjectMenuParentEntity,text="Add\nVertical silder",texture = "white_cube",position = Vec3(1.57, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddThinSliderInScene)
        self.AddObjectFpcButton = Button(name = "Add a FPC in scene",parent = self.AddObjectMenuParentEntity,text="Add FPC\n(First person controller)",texture = "white_cube",position = Vec3(1.75, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddFpcInScene)
        self.AddObjectTpcButton = Button(name = "Add a TPC in scene",parent = self.AddObjectMenuParentEntity,text="Add TPC\n(Third person controller)",texture = "white_cube",position = Vec3(1.93, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddTpcInScene)
        self.AddObjectAbstractionButton = Button(name = "Add an abstraction",parent = self.AddObjectMenuParentEntity,text="Add\nAbstraction",texture = "white_cube",position = Vec3(2.10, -1.02, 0),scale = Vec3(0.1800007, 1, 1),color = color.blue,radius = 0,on_click  = self.AddAbstractionInScene)

    def GetPosTemp(self):
        for i in range(1,len(self.AddObjectMenuParentEntity.children)):
            self.AddObjectMenuParentEntity.children[i].x = self.AddObjectMenuParentEntity.children[i-1].x + 0.18
            # self.AddObjectMenuParentEntity.children[i].color = color.white
            # print(self.AddObjectMenuParentEntity.children[i].x,"  :  ",self.AddObjectMenuParentEntity.children[i].name)
        self.AddObjectMenuParentEntity.add_script(Scrollable(min=len(self.AddObjectMenuParentEntity.children)/-5.3,max=.38,scroll_speed = .03,axis = "x"))


    def AddEntityInScene(self):
        self.WorldItems.append(Entity(name = f"item_{len(self.WorldItems)}",parent = scene,model = "cube",texture = "white_cube",collider = "mesh",collision = True,hovered = True))
        self.ShowObjectContent(self.WorldItems[-1],self.SideBarTopSlideHandler)
        self.ScrollUpdater.update_target("max",34)
        self.ToEditEntity = self.WorldItems[-1]

    def AddButtonInScene(self):
        self.WorldItems.append(Button(name = f"item_{len(self.WorldItems)}",parent = camera.ui,text="Button",model = "cube",texture = "white_cube",scale = .1))
        self.ShowObjectContent(self.WorldItems[-1],self.SideBarTopSlideHandler)
        self.ScrollUpdater.update_target("max",34)
        self.ToEditEntity = self.WorldItems[-1]
        # print_on_screen(self.AddObjectButtonButton.name)

    def AddInputFieldInScene(self): print_on_screen(self.AddObjectInputFieldButton.name)
    def AddTextFieldInScene(self): print_on_screen(self.AddObjectTextFieldButton.name)
    def AddDraggableInScene(self): print_on_screen(self.AddObjectDraggableButton.name)
    def AddDropdownSimpleInScene(self): print_on_screen(self.AddObjectDropdownSimpleButton.name)
    def AddDropdownAdvanceInScene(self): print_on_screen(self.AddObjectDropdownAdvanceButton.name)
    def AddCustomWindowInScene(self): print_on_screen(self.AddObjectCustomWindowButton.name)
    def AddHealthbarInScene(self): print_on_screen(self.AddObjectHealthbarButton.name)
    def AddSliderInScene(self): print_on_screen(self.AddObjectSliderButton.name)
    def AddThinSliderInScene(self): print_on_screen(self.AddObjectThinSliderButton.name)
    def AddFpcInScene(self): print_on_screen(self.AddObjectFpcButton.name)
    def AddTpcInScene(self): print_on_screen(self.AddObjectTpcButton.name)
    def AddAbstractionInScene(self): print_on_screen(self.AddObjectAbstractionButton.name)


    def ShowTabMenu(self):
        if round(self.TabsMenuParentEntity.y,2) == 0.39:
            self.TabsMenuParentEntity.animate_position_y(0.5,.5)
        else:
            self.TabsMenuParentEntity.animate_position_y(0.39,.5)


    def ShowObjectContent(self,Obj,Parent):
        self.TempLen = len(Parent.children)
        print(self.TempLen)
        for i in range(self.TempLen-1,-1,-1):
            destroy(Parent.children[i])
        del self.TempLen
        Parent.children = []


        Parent.children.append(Text(parent = Parent,text =type(Obj).__name__,scale = 3,origin = (0,0),y = .45,z = -100,scale_x = 3.5))
        Parent.children.append(Entity(name = "Line",parent = Parent,model = "line",color = color.black,z = -250,scale = Vec3(0.99, 1.02, 1),position  = Vec3(0.01, 0.39, -250)))

        for i in range(len(self.BasicFunctions)):
            Parent.children.append(Text(parent = Parent,text = f"{self.BasicFunctions[i]}",scale = 2,y = -i*0.08+.36,z = -100,x = -.47))
            Parent.children.append(InputField(name = TextToVar(self.BasicFunctions[i],'_'),parent = Parent,default_value = f"{getattr(Obj,TextToVar(self.BasicFunctions[i],'_'))}",y = -i*0.08+.36,z = -100,x = .1,active = False,text_scale = .75,cursor_y = .1,submit_on='enter',on_submit = Func(self.UpdateItemContent,Obj,Parent)))

    def UpdateItemContent(self,Obj,Parent):
        # Obj.position.x += .2
        # Entity.position_x
        setattr(Obj,"position",(.2,.2,.2))
        for i in range((len(Parent.children))-2):
            if type(Parent.children[i+2]) == InputField:
                setattr(Obj,Parent.children[i+2].name,Parent.children[i+2].text)
                print(f"  :  {Parent.children[i+2].name}  :  {Parent.children[i+2].text}")

        # print(Parent.children)

    def input(self,key):
        print(key)
        if key == "left mouse down":
            if mouse.hovered_entity in self.WorldItems:
            # ray = raycast(mouse.position,camera.forward,ignore=self.WorldGrid).entity
            # print(ray)
                ray = mouse.hovered_entity
                self.ToEditEntity = ray
            # print(mouse.hovered_entity)

        elif key in "right arrow hold":
            try:
                if self.ToEditEntity.parent:
                    self.ToEditEntity.x += self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                # else:
                #     self.ToEditEntity.x += self.PosSnapping3d
                    # print(mouse.hovered_entity.name)

            except:
                print_on_screen("<red>Choose an item to edit")
        elif key in "left arrow hold":
            try:

                if self.ToEditEntity.parent:
                    self.ToEditEntity.x -= self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                # else:
                #     self.ToEditEntity.x += self.PosSnapping3d
            except:
                print_on_screen("<red>Choose an item to edit")
        elif key in "up arrow hold":
            try:
                if self.ToEditEntity.parent:
                    self.ToEditEntity.y += self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                # else:
                #     self.ToEditEntity.x += self.PosSnapping3d
            except:
                print_on_screen("Choose an item to edit",origin=0,color = color.orange)
        elif key in "down arrow hold":
            try:

                if self.ToEditEntity.parent:
                    self.ToEditEntity.y -= self.PosSnapping2d
                    print(mouse.hovered_entity.name)
                # else:
                #     self.ToEditEntity.x += self.PosSnapping3d
            except:
                print_on_screen("<red>Choose an item to edit")

        elif key == "right mouse up" and mouse.hovered_entity in self.WorldItems:
            # if mouse.hovered_entity in self.WorldItems:
                # mouse.hovered_entity
                self.ToEditEntity = mouse.hovered_entity
                # print(self.ToEditEntity)

    def update(self):
        self.WorldGrid[0].scale=distance(camera.position,(0,0,0)) - .4
        
    # def get_hovered_entity(self):
    #     # self.WorldItems = [e for e in level_editor.entities if e]
    #     # [print(str(e)) for e in level_editor.entities]
    #     entities_in_range = [(distance_2d(e.screen_position, mouse.position), e) for e in self.WorldItems]
    #     entities_in_range = [e for e in entities_in_range if e[0] < .03]
    #     entities_in_range.sort()

    #     clicked_entity = None
    #     if entities_in_range:
    #         return entities_in_range[0][1]

    #     # try getting entities with box collider
    #     [setattr(e, 'collision', True) for e in self.WorldItems if not hasattr(e, 'is_gizmo')]
    #     # print('-------------', len([e for e in level_editor.entities  if not hasattr(e, 'is_gizmo') and e.collider and e.collision]))
    #     mouse.update()

    #     if mouse.hovered_entity in self.WorldItems:

    #         [setattr(e, 'collision', False) for e in self.WorldItems if not hasattr(e, 'is_gizmo')]
    #         return mouse.hovered_entity

    #     [setattr(e, 'collision', False) for e in self.WorldItems if not hasattr(e, 'is_gizmo')]

    def MakeEditorEnvironment(self,cam,color,size):

        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0]/255,color[1]/255,color[2]/255,color[3]/255)
        # print(size)
if __name__ == "__main__":
    from OtherStuff import *
    from ursina.camera import Camera
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
    scene_editor = SceneEditor(editor,True,[])
    scene_editor.UniversalParentEntity.enabled = True
    scene_editor.GetPosTemp()
    Sky()

    # camera.ui_display_region.setDimensions(0./2399, .999, 0.1009, 0.938)
    # ui_dr.setDimensions(0.2399, .999, 0.1009, 0.938)
    print(window.screen_resolution)
    scene_editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),((0.2399, .999, 0.1009, 0.938)))
    def input(key):
        if key == "l":
            for i in range(len(camera.ui.children)):
                camera.ui.children[i].enabled = not camera.ui.children[i].enabled
    app.run()


