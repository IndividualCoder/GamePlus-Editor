from ursina import *
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)
from OtherStuff import RecursivePerformer,ReplaceValue
from OpenFile import OpenFile

class FileMenu(Entity):
    '''File menu class, Used by Code editor and UrsaVisor editor, the file system in the UI is made by this class'''
    def __init__(self,ProjectName,Path,parent,CodeEditorEntity: TextField,ShowInstructionFunc,OnFileAdded,queue = 1,z = 0,UdSrc = [],**kwargs):
        super().__init__(*kwargs)

        self.DefaultProjectName = ProjectName
        self.DefaultProjectPath = Path
        self.BackUpUdSrc:list = UdSrc
        self.ShowInstructionFunc = ShowInstructionFunc
        self.CurrentFileName = []
        self.OnFileAdded = OnFileAdded

        self.CodeEditorTextField = CodeEditorEntity
        self.TotalProjectFiles = []
        self.CurrentEditingFileButton: Button = None

        self.UniversalParentEntity = Entity(parent = parent,render_queue = queue,z = z)

        self.TobBarParentEntity = Entity(parent = self.UniversalParentEntity)
        self.FileSystemMenuParentEntity = Entity(parent = self.UniversalParentEntity,y = 0.28)

        self.AddFileButton = Button(name = "AddFileButton",parent = self.TobBarParentEntity,text = "New\nFile",position =  Vec3(0.19, 0.42, z),rotation = Vec3(0, 0, 0),scale = Vec3(0.11, 0.12, 1),render_queue = queue,on_click = self.RegisterFileToEdit)
        self.AddFolderButton = Button(name = "FolderButton",parent = self.TobBarParentEntity,text = "New\nFolder",scale = Vec3(0.11, 0.12, 1),position = Vec3(0.31, 0.42, z),render_queue = queue)
        self.SearchButton = Button(name = "SearchButton",parent = self.TobBarParentEntity,text = "Search",scale =  Vec3(0.11, 0.12, 1),position = Vec3(0.43, 0.42, z),render_queue = queue)

        self.FilesAndButtonSeparator = Entity(name = "separator",parent = self.UniversalParentEntity,model = "line",position =  Vec3(0, 0.33, 0))

        self.SearchButton.text_entity.scale -= .1
        self.AddFileButton.text_entity.scale -= .1
        self.AddFolderButton.text_entity.scale -= .1

        self.WorkingFile = None
        self.WorkingFileLocation = None

    def Show(self,Name = None,Path = None):
        if Path is None:
            Path = self.DefaultProjectPath
        if Name is None:
            Name = self.DefaultProjectName

        for key,value in enumerate(self.BackUpUdSrc):
            self._Temp3 = next(iter(value))
            self.AddFileToEdit(self._Temp3,key)
            self.CurrentFileName.append(self._Temp3)


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

    def RegisterFileToEdit(self):
        self._Temp = len(self.TotalProjectFiles)
        self.CodeEditorTextField.active = False

        def InputFieldToTextFile(Field: InputField):
            if held_keys["enter"]:
                if Field.text in self.CurrentFileName:
                   self.ShowInstructionFunc(Str = "Cannot make another file when a file already exists with that name",Title = "Error")
                else:
                    self.BackUpUdSrc.append({Field.text: ""})
                    self.CurrentFileName.append(Field.text)

                    self.AddFileToEdit(Field.text,len(self.BackUpUdSrc)-1)
                    self.OnFileAdded()

            destroy(Field)

        self._Temp2 = InputField(y = -self._Temp/10,parent = self.FileSystemMenuParentEntity,scale_y = .1,render_queue = self.UniversalParentEntity.render_queue,submit_on=["enter","escape"])

        self._Temp2.on_submit = Func(InputFieldToTextFile,self._Temp2)

    def AddFileToEdit(self,Name: str,CurrentIndex: int):
        self._Temp = len(self.TotalProjectFiles)
        self.TotalProjectFiles.append(Button(text=Name,y = -self._Temp/10,parent = self.FileSystemMenuParentEntity,scale_y = .1,render_queue = self.UniversalParentEntity.render_queue))

        self.TotalProjectFiles[-1].on_click = Func(self.JumpFiles,Name,CurrentIndex,self.TotalProjectFiles[-1])
        self.TotalProjectFiles[-1].text_entity.origin = (-.5,0,0)
        self.TotalProjectFiles[-1].text_entity.position = (-.45,0,0)

        self.TotalProjectFiles[-1].text_entity.render_queue = self.TotalProjectFiles[-1].render_queue


    def JumpFiles(self,FileName,DictIndex,ToJumpFileButton):
        self.CodeEditorTextField.active = True


        if self.CurrentEditingFileButton is not None:
            ReplaceValue(self.CurrentEditingFileButton,ToJumpFileButton)
            ReplaceValue(self.CurrentEditingFileButton,ToJumpFileButton,"highlight_color")
            ReplaceValue(self.CurrentEditingFileButton,ToJumpFileButton,"pressed_color")

            self.CurrentEditingFileButton = ToJumpFileButton
            self.BackUpUdSrc[self.WorkingFileLocation[0]][self.WorkingFileLocation[1]] = self.CodeEditorTextField.text
            self.WorkingFileLocation = (DictIndex,FileName)


        else:
            ToJumpFileButton.color = color.tint(color.orange,-.2)
            ToJumpFileButton.highlight_color = color.tint(ToJumpFileButton.color,.2)
            ToJumpFileButton.pressed_color = color.tint(ToJumpFileButton.color,-.2)
            self.CurrentEditingFileButton = ToJumpFileButton
            self.WorkingFileLocation = (DictIndex,FileName)

        self.CodeEditorTextField.select_all()
        self.CodeEditorTextField.delete_selected()
        self.CodeEditorTextField.text = self.BackUpUdSrc[DictIndex][FileName]

    def  SaveCurrentFile(self):
        if self.CurrentEditingFileButton is not None:
            self.BackUpUdSrc[self.WorkingFileLocation[0]][self.WorkingFileLocation[1]] = self.CodeEditorTextField.text

    def ReCheckCodeFiles(self):
        for key,value in enumerate(self.BackUpUdSrc):
            self._Temp3 = next(iter(value))
            if self._Temp3 not in self.CurrentFileName:
                self.AddFileToEdit(self._Temp3,key)
                self.CurrentFileName.append(self._Temp3)


if __name__ == "__main__":
    # def CurrentFolderNameReturner():
        # return os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
    # print(ValueToString(True))

    app = Ursina()
    from OtherStuff import CurrentFolderNameReturner
    a = FileMenu("jh",f"{CurrentFolderNameReturner()}Current Games",Entity())
    a.SetUp()
    a.Show()

    app.run()
