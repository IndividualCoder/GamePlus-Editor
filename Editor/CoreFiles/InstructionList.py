class InstructionList(list):
    def append(self,item):
        super().insert(0,item)
        for i in range(1,len(self)):
            self[i].Up(self[i-1])

