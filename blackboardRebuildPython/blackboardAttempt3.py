#threading library handles running multiple things at once
import threading
#time library used for timestamps
import time

class Blackboard():
    
    #-----------------------------------------------------------------
    def __init__(self):
        
        #main dictionary w label : list of values earliest->latest
        self.__info = {}
        #dictionary w label : time when it was last updated
        self.__timestamps = {}
        #a waiting room for threads to sit in until they're notified something has changed
        self.__condition = threading.Condition()
        
   
    
    #-----------------------------------------------------------------
    def post(self, postLabel, postData):
        
        #acquires a lock on the condition, so only one thread can be inside the block at a time
        #so if 2 things try to post at the same time, one waits for the other to finish
        with self.__condition:
            if postLabel not in self.__info:
                self.__info[postLabel] = [postData]
            else:
                self.__info[postLabel].append(postData)
                
            #record the time of the posting (puts it as a float)
            self.__timestamps[postLabel] = time.time()
            
            #notify all components in waiting room that a new post has been made
            #tells them to wake up and check if there's anything they were waiting for
            self.__condition.notify_all()
            
     
   
    #-----------------------------------------------------------------
    def get(self, targetLabel, index):
        
        #checking if the label exists
        hasLabel = targetLabel in self.__info
                
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
        
    
    
    #-----------------------------------------------------------------
    #handles thread pausing to wait until new data comes out about one of the labels it cares abt
    #subscriptions = list of labels it cares abt/subscribes to
    #last_stamps = list of timestamps the caller already knows abt, so anything later is new data
    def wait(self, subscriptions, rememberedStamps = None):
        
        #acquires a lock on the condition, so only one thread can be inside the block at a time
        #only one thread has access while it checks for new data
        with self.__condition:
            while True:
                #i is the index of each label in labels
                for i, label in enumerate(subscriptions):
                    #see what time the most recent post to this label was made (default 0 if never posted)
                    blackboardStamp = self.__timestamps.get(label, 0)
                    #seeing the most recent post that the caller remembers (default 0 if doesn't exist)
                    callerStamp = 0
                    #if caller remembers any stamps and remembers a stamp for that label
                    if rememberedStamps && rememberedStamps[i]:
                        callerStamp = rememberedStamps[i]
                        
                    #if that label has been updated with new info, return it
                    if blackBoardStamp > callerStamp:
                        return label 
                
                #if not, keep waiting
                self.__condition.wait()
                
        

