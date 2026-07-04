class Blackboard():
    def __init__(self):
        self.__visionData = []
        self.__memoryData = []
        
    #posting
    
    def addToVision(self, newVision):
        visionData.append(newVision)
        
    def addToMemory(self, newMemory):
        memoryData.append(newMemory)
        
    #reading
        
    def getCurrentVision(self):
        return self.__visionData[-1]
    
    def getCurrentMemory(self):
        return self.__memoryData[-1]
