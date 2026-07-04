class Blackboard():
    def __init__(self):
        #main dictionary w label : list of values earliest->latest
        self.__info = {}
        
        
    def post(self, postLabel, postData):
        #checking if the label already exists
        hasLabel = False
        for label in self.__info.keys():
            if(label == postLabel):
                hasLabel = True
        #if doesn't exist make it a new dict entry        
        if(!hasLabel):
            newList = []
            newList.append(postData)
            self.__info[postLabel] = newList
        #if does exist add to current dict entry
        else:
            self.__info[postLabel].append(postData)
            
    def get(self, targetLabel, index):
        #checking if the label exists
        hasLabel = False
        for label in self.__info.keys():
            if(label == targetLabel):
                hasLabel = True
                
        #if label doesn't exist, give an error message
        if(!hasLabel):
            print("Error! requested label not found")
            return None
        else:
            dataList = self.__info[targetLabel]
            #check if index is valid and return it or give error
            try:
                return dataList[index]
            except IndexError:
                print("Error! " + (str)(index) + " is an invalid index")       
    
    def wait(self, 
            
            
        