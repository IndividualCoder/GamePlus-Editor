from ursina import *
from DirectionBox import PointOfViewSelector as DirectionEntity
from OtherStuff import TextToVar,MultiFunctionCaller
from ursina.color import tint
from ColorMenu import ColorMenu

class SceneEditor(Entity):
    def __init__(self,enabled,SaveFunction,AddTerminalFunc,EditorCamera,EditorDataDict,cam2 = camera,CurrentProjectName = "",**kwargs):
        super().__init__(kwargs)

        self.WorldItems = []
        self.Save = SaveFunction
        self.AddTerminal = AddTerminalFunc
        self.CurrentProjectName = CurrentProjectName
        self.EditorCamera = EditorCamera
        self.IsEditing = True
        self.EditorDataDict = EditorDataDict

        self.AddObjectTextList = ["Add static object","Add dynamic object","Add FPC","Add TPC","Add abstraction"]
        self.AddObjectOnClickFuncList = [self.AddEntityInScene,self.AddEntityInScene,self.AddEntityInScene,self.AddEntityInScene,self.AddEntityInScene]
        self.BasicFunctions = ["Position x: ","Position y: ","Position z: ","Rotation x: ","Rotation y: ","Rotation z: ","Scale x: ","Scale y: ","Scale z: ","Color: ","Texture: "]
        self.SpecialFunctions:list = ["Color: "]
        self.ToEditEntity = None
        self.PosSnapping2d = .01
        self.PosSnapping3d = .7

        self.UniversalParentEntity = Entity(parent = cam2.ui,enabled = False)
        self.SideBarTopParentEntity = Entity(parent = self.UniversalParentEntity,model = "cube",enabled = enabled,position = Vec3(-0.68, 0.16, 10),scale = Vec3(0.43, 0.56, 2),color = color.gray)
        self.AddObjectMenuParentEntity = Entity(parent = self.UniversalParentEntity,model = None,enabled = enabled,position = Vec3(0.38, -0.35, 2),scale = Vec3(1.69, 0.1, 1),color = color.dark_gray,origin_y = 1)
        self.SideBarBottomParentEntity = Entity(parent = self.UniversalParentEntity,model = "cube",enabled = enabled,position = Vec3(-0.68, -0.31, -200),scale = Vec3(0.43, 0.38, 2),color = color.tint(color.gray,-.1),collider = "mesh")

        self.SideBarTopSlideHandler = Button(parent = self.SideBarTopParentEntity,model = "cube",radius=0,visible_self = False,z = -200)


        # self.ToImport.add("from ursina import *")

        # self.SideBarTopSlider = Entity(parent = self.SideBarTopSlideHandler,model = "cube",visible_self = False,z = -202)
        self.ScrollUpdater = self.SideBarTopSlideHandler.add_script(Scrollable(min=-.1,max = .3,scroll_speed = .01))


        self.WorldGrid = [Entity(parent=self, model=Grid(200,200,thickness = 2), rotation_x=90, scale=Vec3(200, 200, 200), collider=None, color=color.red),Entity(parent=self, model=Grid(100,100,thickness = 3), rotation_x=90, scale=Vec3(200, 200, 200), collider=None, color=color.black33),Entity(parent=self, model=Grid(400,400), rotation_x=90, scale=Vec3(40, 40, 40), collider=None, color=color.green)]
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
        self.WorldItems.append(Entity(name = f"item_{len(self.WorldItems)}",parent = scene,model = "cube",texture = "white_cube",collider = "mesh",collision = True,color = color.white))
        self.ShowObjectContent(self.WorldItems[-1],self.SideBarTopSlideHandler)
        self.ScrollUpdater.update_target("max",34)
        self.ToEditEntity = self.WorldItems[-1]


    def ShowObjectContent(self,Obj,Parent: Entity):
        self.TempLen = len(Parent.children)
        for i in range(self.TempLen-1,-1,-1):
            destroy(Parent.children[i])
        del self.TempLen
        Parent.children = []


        Parent.children.append(Text(parent = Parent,text =type(Obj).__name__,scale = 3,origin = (0,0),y = .45,z = 20,scale_x = 3.5))
        Parent.children.append(Entity(name = "Line",parent = Parent,model = "line",color = color.black,scale = Vec3(0.99, 1.02, 1),position  = Vec3(0.01, 0.39, 20)))

        for i in range(len(self.BasicFunctions)):
            Text(parent = Parent,text = f"{self.BasicFunctions[i]}",scale = 2,y = -i*0.08+.36,z = 20,x = -.47)

        for i in range(len(self.BasicFunctions)):
            if self.BasicFunctions[i]  in self.SpecialFunctions:
                j = self.SpecialFunctions.index(self.BasicFunctions[i])
                if self.SpecialFunctions[j] == "Color: ":
                    ColorMenu(Obj,(2.5,15),BGPos=(1,1),scale = (.5,.05),parent = Parent,y = -i*0.08+.36,z = -20,x = .1,radius = 1).SetUp()

            else:
                InputField(name = TextToVar(self.BasicFunctions[i],'_'),submit_on=["enter","escape"],parent = Parent,default_value = f"{getattr(Obj,TextToVar(self.BasicFunctions[i],'_'))}",y = -i*0.08+.36,z = -20,x = .1,active = False,text_scale = .75,cursor_y = .1,enter_active = True,on_submit = Func(self.UpdateItemContent,Obj,Parent))
            # Parent.children[-1].update = Func(MultiFunctionCaller,Func(setattr,Parent.children[-1],"text",getattr(Obj,TextToVar(self.BasicFunctions[i],'_'))))

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
        if not self.IsEditing:
            return

        elif key == "`":
            self.TerminalIndex = [i for i in self.UniversalParentEntity.children if i.name == "Terminal"]

            if self.TerminalIndex == []:
                self.AddTerminal()
                self.TerminalIndex = [i for i in self.UniversalParentEntity.children if i.name == "Terminal"]

            else:
                self.TerminalIndex[0].Toogle()

        elif key in ["left mouse"]:
            if mouse.hovered_entity in self.WorldItems:
                if mouse.hovered_entity == self.ToEditEntity:
                    return

                self.ToEditEntity =  mouse.hovered_entity
                self.ShowObjectContent(self.ToEditEntity,self.SideBarTopSlideHandler)

        elif key in ["right arrow","right arrow hold"]:
            try:
                self.ToEditEntity.x += self.PosSnapping2d

            except AttributeError:
                print_on_screen("<color:red>Choose an item to edit")
        elif key in ["left arrow","left arrow hold"]:
            try:

                self.ToEditEntity.x -= self.PosSnapping2d
            except AttributeError:
                print_on_screen("<color:red>Choose an item to edit")
        elif key in ["up arrow","up arrow hold"]:
            try:
                self.ToEditEntity.y += self.PosSnapping2d
            except AttributeError:
                print_on_screen("<color:red>Choose an item to edit")
        elif key in ["down arrow","down arrow hold"]:
            try:
                self.ToEditEntity.y -= self.PosSnapping2d
            except AttributeError:
                print_on_screen("<color:red>Choose an item to edit")

        elif key == "right mouse up" and mouse.hovered_entity in self.WorldItems:
                self.ToEditEntity = mouse.hovered_entity

        elif key == "delete up":
            try:
                index = self.WorldItems.index(self.ToEditEntity)
                destroy(self.ToEditEntity)
                del self.WorldItems[index]
                self.ToEditEntity = None
            except ValueError:
                pass

    def update(self):
        if not self.IsEditing:
            return

        if 1 < distance(camera.position,(0,0,0)):
            self.distance = distance(camera.position,(0,0,0))
            if self.distance > 150:
                self.distance = 150
        else:
            self.distance = 0

        if self.distance > 10:
            self.WorldGrid[0].color = color.rgba(70,70,70,1000 / self.distance)
            if int(self.WorldGrid[0].color[3]) == 0 and self.distance < 50: self.WorldGrid[0].enable()

            self.WorldGrid[1].color = color.rgba(50,50,50,self.distance)
            if int(self.WorldGrid[1].color[3]) == 0: self.WorldGrid[1].enable()

            self.WorldGrid[2].color = color.rgba(0,0,0,200/self.distance)
            if int(self.WorldGrid[2].color[3]) == 0 and self.distance < 50: self.WorldGrid[2].enable()

        if self.distance < 10:
            self.WorldGrid[1].color = color.rgba(50,50,50,0)
            self.WorldGrid[1].disable()

        if self.distance > 50:
            self.WorldGrid[2].color = color.rgba(0,0,0,0)
            self.WorldGrid[2].disable()
            self.WorldGrid[0].color = (70,70,70,0)
            self.WorldGrid[0].disable()

            # print(self.distance)

            # if self.distance != 0:
            #     if int(self.WorldGrid[0].color[3]) * 255 == 0: self.WorldGrid[0].disable()
            #     if int(self.WorldGrid[1].color[3]) * 255 == 0: self.WorldGrid[1].disable()
            #     if int(self.WorldGrid[2].color[3]) * 255 == 0: self.WorldGrid[2].disable()

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

        self.ConfigEditorAsSettings(self.EditorDataDict)

    def SaveEditor(self):
        self.Save()

    def ConfigEditorAsSettings(self,DataDict):
        self.SetTooltip(DataDict["Show tooltip"])

    def SetTooltip(self,value):
        self.ItemToToolTipList = []
        if value:
            self.ToolTipList = []
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = Tooltip(self.ToolTipList[i],z = -30,render_queue = 2,always_on_top = True)
                # self.ItemToToolTipList[i].tool_tip.background.z = -1

        else:
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = None

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
    scene_editor = SceneEditor(editor_camera=editor,enabled=True,WorldItems=[],ToImport=set(),EditorCamera=editor,SaveFunction=Func(print,"hele"),ShowInstructionFunc=Func(print,"hele"),EditorDataDict={"Hell": 1})
    scene_editor.UniversalParentEntity.enabled = True
    scene_editor.GetPosTemp()
    Sky()

    # camera.ui_display_region.setDimensions(0./2399, .999, 0.1009, 0.938)
    # ui_dr.setDimensions(0.2399, .999, 0.1009, 0.938)
    # print(window.screen_resolution)
    print(application.base.camNode.getDisplayRegion(0))
    '''0.2399, .999, 0.1009, 0.938'''
    scene_editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, 1, 0.1009, 0.938))

    def input(key):
        if key == "l":
            for i in range(len(camera.ui.children)):
                camera.ui.children[i].enabled = not camera.ui.children[i].enabled
        if key == "q":
            application.quit()
    app.run()

