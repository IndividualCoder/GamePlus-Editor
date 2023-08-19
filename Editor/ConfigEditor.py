import os
import json
def ConfigEditorWrite(vars,values):
    FolderName = os.path.dirname(os.path.abspath(__file__))
    FolderName = FolderName.replace("\\","/")
    FolderName = FolderName.replace("Editor","EditorConfig")

    # print(FolderName)
    if not os.path.isdir(FolderName):
        os.makedirs(FolderName)
        # print(FolderName," s")
        # return

    # with open(f"{FolderName}/Config editor.txt","w"):
    #     for i in range(len(vars)):
            


if __name__ == "__main__":
    ConfigEditorWrite()