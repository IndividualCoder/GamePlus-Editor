from ursina import *
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)
from OtherStuff import RecursivePerformer

class FileMenu(Entity):
    '''File menu class, Used by Code editor and UrsaVisor editor, the file system in the UI is made by this class'''
    def __init__(self,ProjectName,Path,parent,queue = 1,z = 0,**kwargs):
        super().__init__(*kwargs)
        if ProjectName is not None:
            self.Show(ProjectName,Path)


        self.UniversalParentEntity = Entity(parent = parent,render_queue = queue)

        self.TobBarParentEntity = Entity(parent = self.UniversalParentEntity)
        self.FileSystemMenuParentEntity = Entity(parent = self.UniversalParentEntity)

        self.AddFileButton = Button(name = "AddFileButton",parent = self.TobBarParentEntity,text = "New\nFile",position =  Vec3(0.22, 0.42, z),rotation = Vec3(0, 0, 0),scale = Vec3(0.1, 0.12, 1),render_queue = queue)
        self.AddFolderButton = Button(name = "FolderButton",parent = self.TobBarParentEntity,text = "New\nFolder",scale = Vec3(0.1, 0.12, 1),position = Vec3(0.33, 0.42, z),render_queue = queue)
        self.SearchButton = Button(name = "SearchButton",parent = self.TobBarParentEntity,text = "Search",scale =  Vec3(0.1, 0.12, 1),position = Vec3(0.44, 0.42, z),render_queue = queue)

        self.TempButton  = Button(scale = (0,0),Key="p",on_key_press=Func(RecursivePerformer,self.UniversalParentEntity,self.ShowPosTemp,BasicFunc = False))

    #     Button(scale = (0,0),Key=["1","1 hold"],on_key_press=Func(self.SetUpProperty,self.ToEdit,"scale_y",.01))
    #     Button(scale = (0,0),Key=["2","2 hold"],on_key_press=Func(self.SetUpProperty,self.ToEdit,"scale_y",-.01))
    #     Button(scale = (0,0),Key=["3","3 hold"],on_key_press=Func(self.SetUpProperty,self.ToEdit,"scale_x",.01))
    #     Button(scale = (0,0),Key=["4","4 hold"],on_key_press=Func(self.SetUpProperty,self.ToEdit,"scale_x",-.01))

        # Button(scale = (0,0),Key=["i","i hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"y",.01))
        # Button(scale = (0,0),Key=["k","k hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"y",-.01))
        # Button(scale = (0,0),Key=["j","j hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"x",-.01))
        # Button(scale = (0,0),Key=["l","l hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"x",.01))
        # Button(scale = (0,0),Key=["up arrow","up arrow hold"],on_key_press=Func(self.SetUpProperty,self.AddFileButton,"y",.01))
        # Button(scale = (0,0),Key=["down arrow","down arrow hold"],on_key_press=Func(self.SetUpProperty,self.AddFileButton,"y",-.01))
        # Button(scale = (0,0),Key=["left arrow","left arrow hold"],on_key_press=Func(self.SetUpProperty,self.AddFileButton,"x",-.01))
        # Button(scale = (0,0),Key=["right arrow","right arrow hold"],on_key_press=Func(self.SetUpProperty,self.AddFileButton,"x",.01))

    #     Button(scale = (0,0),Key=["5","5 hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"scale_y",.01))
    #     Button(scale = (0,0),Key=["6","6 hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"scale_y",-.01))
    #     Button(scale = (0,0),Key=["7","7 hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"scale_x",.01))
    #     Button(scale = (0,0),Key=["8","8 hold"],on_key_press=Func(self.SetUpProperty,self.AddFolderButton,"scale_x",-.01))

        # Button(scale = (0,0),Key="x",on_key_press=Func(self.SetEdit,self.AddFileButton))
        # Button(scale = (0,0),Key="y",on_key_press=Func(self.SetEdit,self.AddFolderButton))
        # Button(scale = (0,0),Key="z",on_key_press=Func(self.SetEdit,self.SearchButton))

    # def SetEdit(self,Entity):
    #     self.ToEdit = Entity



    def ShowPosTemp(self,Entity):
        print(f"{__file__}:: Name: {Entity.name}, position =  {Entity.position},rotation = {Entity.rotation},scale = {Entity.scale} ")



    def SetUpProperty(self,Entity,val,ToSubOrAdd):
        setattr(Entity,val,getattr(Entity,val) + ToSubOrAdd)

    def Show(self,Name,Path):
        # try:
        #     with open(f"{Name}/{Path}") as ProjectFile:
        #         self.
        ...
    def SetUp(self):
        '''Sets up the class'''
        self.AddFileButton.text_entity.render_queue = self.AddFileButton.render_queue
        self.AddFolderButton.text_entity.render_queue = self.AddFolderButton.render_queue
        self.SearchButton.text_entity.render_queue = self.SearchButton.render_queue

        self.AddFileButton.text_entity.scale = .5
        self.AddFolderButton.text_entity.scale = .5
        self.SearchButton.text_entity.scale = .5
        def SetRenderQueue(Entity):
            Entity.render_queue = self.UniversalParentEntity.render_queue
        RecursivePerformer(self.UniversalParentEntity.children,ToPerform=SetRenderQueue,BasicFunc=False)


if __name__ == "__main__":
    # def CurrentFolderNameReturner():
        # return os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
    # print(ValueToString(True))
    app = Ursina()
    from OtherStuff import CurrentFolderNameReturner
    FileMenu("a",CurrentFolderNameReturner().replace("Editor","Current Games"),Entity()).SetUp()
    app.run()
