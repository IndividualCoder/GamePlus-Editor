#Starting ui
    # self.TempButton  = Button(scale = (0,0),Key="p",on_key_press=self.ShowPosTemp)

    # self.TempButton3 = Button(scale = (0,0),Key=["a","a hold"],on_key_press=self.ChangeTitleFieldPositionXN)
    # self.TempButton4 = Button(scale = (0,0),Key=["d","d hold"],on_key_press=self.ChangeTitleFieldPositionXP)
    # self.TempButton5 = Button(scale = (0,0),Key=["w","w hold"],on_key_press=self.ChangeTitleFieldPositionYP)
    # self.TempButton6 = Button(scale = (0,0),Key=["s","s hold"],on_key_press=self.ChangeTitleFieldPositionYN)

    # self.TempButton7 = Button(scale = (0,0),Key=["left arrow","left arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionXN)
    # self.TempButton8 = Button(scale = (0,0),Key=["right arrow","right arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionXP)
    # self.TempButton9 = Button(scale = (0,0),Key=["up arrow","up arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionYP)
    # self.TempButton10 = Button(scale = (0,0),Key=["down arrow","down arrow hold"],on_key_press=self.ChangeDescriptionFieldPositionYN)

    # self.TempButton11 = Button(scale = (0,0),Key=["z","z hold"],on_key_press=self.ChangeDescriptionFieldPositionXN2)
    # self.TempButton12 = Button(scale = (0,0),Key=["x","x hold"],on_key_press=self.ChangeDescriptionFieldPositionXP2)
    # self.TempButton13 = Button(scale = (0,0),Key=["c","c hold"],on_key_press=self.ChangeDescriptionFieldPositionYP2)
    # self.TempButton14 = Button(scale = (0,0),Key=["v","v hold"],on_key_press=self.ChangeDescriptionFieldPositionYN2)

    # self.TempButton15  = Button(scale = (0,0),Key=["1","1 hold"],on_key_press=self.ScaleUpX)
    # self.TempButton16  = Button(scale = (0,0),Key=["2","2 hold"],on_key_press=self.ScaleUpY)
    # self.TempButton17  = Button(scale = (0,0),Key=["3","3 hold"],on_key_press=self.ScaleUpX2)
    # self.TempButton18  = Button(scale = (0,0),Key=["4","4 hold"],on_key_press=self.ScaleUpY2)

    # self.TempButton19  = Button(scale = (0,0),Key=["5","5 hold"],on_key_press=self.ScaleUpX3)
    # self.TempButton20  = Button(scale = (0,0),Key=["6","6 hold"],on_key_press=self.ScaleUpY3)
    # self.TempButton21  = Button(scale = (0,0),Key=["7","7 hold"],on_key_press=self.ScaleUpX4)
    # self.TempButton22  = Button(scale = (0,0),Key=["8","8 hold"],on_key_press=self.ScaleUpY4)

def ShowPosTemp(self):
    for i in range(len(self.CreateNewProjectMenuParentEntity.children)):
        print(f'name: {self.CreateNewProjectMenuParentEntity.children[i].name},pos:{self.CreateNewProjectMenuParentEntity.children[i].position},Scale:{self.CreateNewProjectMenuParentEntity.children[i].scale}')

def ScaleUpX(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityLowButton.x -= .01

def ScaleUpY(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityLowButton.y -= .01

def ScaleUpX2(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityLowButton.x += .01

def ScaleUpY2(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityLowButton.y += .01

def ScaleUpX3(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityMediumButton.x -= .01

def ScaleUpY3(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityMediumButton.y -= .01

def ScaleUpX4(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityMediumButton.x += .01

def ScaleUpY4(self):
    # for i in range(len(self.ChangeVarsMenuParentEntity.children)):
    self.ProjectGraphicsQualityMediumButton.y += .01


def ChangeTitleFieldPositionXP(self):
    self.ProjectGraphicsQualityHighButton.x += .005

def ChangeTitleFieldPositionXN(self):
    self.ProjectGraphicsQualityHighButton.x -= .005

def ChangeTitleFieldPositionYP(self):
    self.ProjectGraphicsQualityHighButton.y += .005

def ChangeTitleFieldPositionYN(self):
    self.ProjectGraphicsQualityHighButton.y -= .005


def ChangeDescriptionFieldPositionXP(self):
    self.ProjectGraphicsQualityMediumButton.x += .01

def ChangeDescriptionFieldPositionXN(self):
    self.ProjectGraphicsQualityMediumButton.x -= .01

def ChangeDescriptionFieldPositionYP(self):
    self.ProjectGraphicsQualityMediumButton.y += .01

def ChangeDescriptionFieldPositionYN(self):
    self.ProjectGraphicsQualityMediumButton.y -= .01


def ChangeDescriptionFieldPositionXP2(self):
    self.ProjectGraphicsQualityHighButton.x += .01

def ChangeDescriptionFieldPositionXN2(self):
    self.ProjectGraphicsQualityHighButton.x -= .01

def ChangeDescriptionFieldPositionYP2(self):
    self.ProjectGraphicsQualityHighButton.y += .01

def ChangeDescriptionFieldPositionYN2(self):
    self.ProjectGraphicsQualityHighButton.y -= .01


#ScenEditor
        self.ShowPosTempButton = Button(Key="p",on_key_press=self.ShowPosTemp,on_click = self.ShowPosTemp,scale= 0)
        # self.AddObjectButton = Button(parent = self.AddObjectMenuParentEntity,scale = (.01,.01))
        # self.QuitTempButton = Button(Key="q",on_key_press=application.quit,on_click = self.ShowPosTemp,scale= (0,0))
        # self.QuitTempButton = Button(Key="i",on_key_press=self.GetPosTemp,on_click = self.GetPosTemp,scale= (0,0))
 

        # self.Temp1 = Button(Key=["1","1 hold"],on_key_press=self.UpdateScaleXP,scale = 0)
        # self.Temp2 = Button(Key=["2","2 hold"],on_key_press=self.UpdateScaleXN,scale = 0)
        # self.Temp3 = Button(Key=["3","3 hold"],on_key_press=self.UpdateScaleYP,scale = 0)
        # self.Temp4 = Button(Key=["4","4 hold"],on_key_press=self.UpdateScaleYN,scale = 0)

        # self.Temp5 = Button(Key=["1","1 hold"],on_key_press=self.UpdatePosXP,scale = 0)
        # self.Temp6 = Button(Key=["2","2 hold"],on_key_press=self.UpdatePosXN,scale = 0)
        # self.Temp7 = Button(Key=["3","3 hold"],on_key_press=self.UpdatePosYP,scale = 0)
        # self.Temp8 = Button(Key=["4","4 hold"],on_key_press=self.UpdatePosYN,scale = 0)

        # self.Temp5 = Button(Key=["d","d hold"],on_key_press=self.UpdatePosXP2,scale = 0)
        # self.Temp6 = Button(Key=["a","a hold"],on_key_press=self.UpdatePosXN2,scale = 0)
        # self.Temp7 = Button(Key=["w","w hold"],on_key_press=self.UpdatePosYP2,scale = 0)
        # self.Temp8 = Button(Key=["s","s hold"],on_key_press=self.UpdatePosYN2,scale = 0)



    def ShowPosTemp(self):
        # for i in range(len(self.SideBarTopParentEntity.children)):
        #     print(self.SideBarTopParentEntity.children[i].position,end="")
        #     print(self.SideBarTopParentEntity.children[i].scale,end="")
        #     print(self.SideBarTopParentEntity.children[i].name)
        print(self.WorldItems)
        # print(self.AddObjectButtonButton.position)
        # print(self.AddObjectButtonButton.scale)


    def UpdatePosXP(self):
        self.Text3.scale_x += .01
    def UpdatePosXN(self):
        self.Text3.scale_x -= .01
    def UpdatePosYP(self):
        self.Text3.scale_y += .01
    def UpdatePosYN(self):
        self.Text3.scale_y -= .01

    def UpdatePosXP2(self):
        self.Text3.x += .01
    def UpdatePosXN2(self):
        self.Text3.x -= .01
    def UpdatePosYP2(self):
        self.Text3.y += .01
    def UpdatePosYN2(self):
        self.Text3.y -= .01

    def UpdateScaleXP(self):
        self.Text2.x += .01
    def UpdateScaleXN(self):
        self.Text2.x -= .01
    def UpdateScaleYP(self):
        self.Text2.y += .01
    def UpdateScaleYN(self):
        self.Text2.y -= .01
