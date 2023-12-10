from GamePlusEditor.ursina import *
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)
from GamePlusEditor.OtherStuff import RecursivePerformer,ReplaceValue

class FileMenu(Entity):
    '''Used by CodeEditorPython that Operates file system and data saving into it'''
    def __init__(self,ProjectName,Path,parent,CodeEditorEntity: TextField,ShowInstructionFunc,OnFileAdded,queue = 1,z = 0,UdSrc = [],**kwargs) -> None:
        super().__init__(*kwargs)

        self.DefaultProjectName: str = ProjectName
        self.DefaultProjectPath: str = Path
        self.BackUpUdSrc:list = UdSrc
        self.ShowInstructionFunc: function = ShowInstructionFunc
        self.CurrentFileName: list = []
        self.OnFileAdded: function = OnFileAdded

        self.CodeEditorTextField: InputField = CodeEditorEntity
        self.TotalProjectFiles: list = []
        self.CurrentEditingFileButton: Button = None

        self.UniversalParentEntity: Entity = Entity(parent = parent,render_queue = queue,z = z)

        self.TobBarParentEntity: Entity = Entity(parent = self.UniversalParentEntity)
        self.FileSystemMenuParentEntity: Entity = Entity(parent = self.UniversalParentEntity,y = 0.28)

        self.AddFileButton: Button = Button(name = "AddFileButton",parent = self.TobBarParentEntity,text = "New\nFile",position =  Vec3(0.19, 0.42, z),rotation = Vec3(0, 0, 0),scale = Vec3(0.11, 0.12, 1),render_queue = queue,on_click = self.RegisterFileToEdit)
        self.AddFolderButton: Button = Button(name = "FolderButton",parent = self.TobBarParentEntity,text = "New\nFolder",scale = Vec3(0.11, 0.12, 1),position = Vec3(0.31, 0.42, z),render_queue = queue)
        self.SearchButton: Button = Button(name = "SearchButton",parent = self.TobBarParentEntity,text = "Search",scale =  Vec3(0.11, 0.12, 1),position = Vec3(0.43, 0.42, z),render_queue = queue)

        self.FilesAndButtonSeparator: Entity = Entity(name = "separator",parent = self.UniversalParentEntity,model = "line",position =  Vec3(0, 0.33, 0))

        self.SearchButton.text_entity.scale -= .1
        self.AddFileButton.text_entity.scale -= .1
        self.AddFolderButton.text_entity.scale -= .1

        self.WorkingFile: str = None
        self.WorkingFileLocation: str = None

    def Show(self,Name = None,Path = None) -> None:
        '''Opens filesystem of given name and path'''
        if Path is None:
            Path = self.DefaultProjectPath
        if Name is None:
            Name = self.DefaultProjectName

        for key,value in enumerate(self.BackUpUdSrc):
            self._Temp3 = next(iter(value))
            self.AddFileToEdit(self._Temp3,key)
            self.CurrentFileName.append(self._Temp3)

    def CheckSyntax(self,Code) -> bool:
        '''Checks if the given code is valid python syntax or not'''
        try:
            compile(Code, "string", "exec")
            return True  
        except SyntaxError:
            return False  


    def SetUp(self) -> None:
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

    def RegisterFileToEdit(self) -> None:
        '''Registers to add a new file\nAdds a temp input field to get the filename if the given name does not already exists, runs the `AddFileToEdit` function'''
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

    def AddFileToEdit(self,Name: str,CurrentIndex: int) -> None:
        '''Adds a new file to the project'''
        self._Temp = len(self.TotalProjectFiles)
        self.TotalProjectFiles.append(Button(text=Name,y = -self._Temp/10,parent = self.FileSystemMenuParentEntity,scale_y = .1,render_queue = self.UniversalParentEntity.render_queue))

        self.TotalProjectFiles[-1].on_click = Func(self.JumpFiles,Name,CurrentIndex,self.TotalProjectFiles[-1])
        self.TotalProjectFiles[-1].text_entity.origin = (-.5,0,0)
        self.TotalProjectFiles[-1].text_entity.position = (-.45,0,0)

        self.TotalProjectFiles[-1].text_entity.render_queue = self.TotalProjectFiles[-1].render_queue


    def JumpFiles(self,FileName,DictIndex,ToJumpFileButton) -> None:
        '''Jumps between files'''
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

    def  SaveCurrentFile(self) -> None:
        '''Saves current file that is being edited'''
        if self.CurrentEditingFileButton is not None:
            self.BackUpUdSrc[self.WorkingFileLocation[0]][self.WorkingFileLocation[1]] = self.CodeEditorTextField.text

    def ReCheckCodeFiles(self) -> None:
        '''If more than one FileMenu exists, Adding a file in one of them may not be updated in the other\nThis funciton confirms that'''
        for key,value in enumerate(self.BackUpUdSrc):
            self._Temp3 = next(iter(value))
            if self._Temp3 not in self.CurrentFileName:
                self.AddFileToEdit(self._Temp3,key)
                self.CurrentFileName.append(self._Temp3)


if __name__ == "__main__":

    app = Ursina()
    from GamePlusEditor.OtherStuff import CurrentFolderNameReturner
    a = FileMenu("jh",f"{CurrentFolderNameReturner()}Current Games",Entity())
    a.SetUp()
    a.Show()

    app.run()
