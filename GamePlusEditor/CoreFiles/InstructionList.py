class InstructionList(list):
    '''A simple list that overwrites the .append method and adds item to the first index\nUsed for InstructionMenu to go upwards'''
    def append(self,item) -> None:
        super().insert(0,item)
        for i in range(1,len(self)):
            self[i].Up(self[i-1])

