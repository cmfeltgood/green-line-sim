from train import TrainQueue, Train, State
from collections.abc import Callable
import random


#NOTE: Currently, no implementation of speed limits. Assumed 44ft/s
class Track:
    def __init__(self, id=-1, len=1000, speedLimit=44):
        self._trains:TrainQueue = TrainQueue()
        self._next:Track = None
        self._len: float = len
        self._speedLimit: float = speedLimit
        self._id = id

    def tick(self):
        """Instructions for each second"""
        needsPopped = 0

        for t in self._trains:
            #Check for needed state of train
            speed, dist = self.getNextSpeedChange(t)
            if speed == None:
                t.accelerate()
            else:
                t.targetSpeed(dist, speed)

            t.tick()
            #print(f"{t} on track {self._id}")

            #check if needs to move on
            if t.getPosition() > self._len:
                needsPopped += 1
                t.setPosition(t.getPosition()-self._len)
        
        self._next.tick()

        #trains should still be in order
        #NOTE: Make sure trains are in order
        for i in range(needsPopped):
            self._next.addTrain(self._trains.pop())

            

    def getNext(self)->'Track':
        """Get next track"""
        return self._next

    def setNext(self, next:'Track')->None:
        """Set next track"""
        self._next = next
    
    def addTrain(self, train:Train)->None:
        """Add train to this track segment"""
        self._trains.add(train)
        train.setMaxSpeed(self._speedLimit)
    
    def getNextSpeedChange(self, t:Train)->tuple[float, float]:
        """Returns the speed of and distance to the next speed change"""
        f = t.getStoppingLine()
        len = self._len - t.getPosition()
        if len > 500:
            return None, None
        else:
            return self.getNext().gnscRec(f, len, -1, None, None)
    
    def gnscRec(self, f:Callable[[float],tuple[float,float]], len:float, diff:float, speed:float, dist:float)->tuple[float, float]:
        """Recursive helper function for getNextSpeedChange()"""
        if speed == None or self._speedLimit < speed:
            min, max = f(self._speedLimit)
            if min <= len and max >= len:
                newDiff = len - min
                if newDiff > diff:
                    if len > 500:
                        return self._speedLimit, len
                    else:
                        return self.getNext().gnscRec(f, len+self._len, newDiff, self._speedLimit, len)

        len+=self._len
        if len > 500:
            return speed, dist
        else:
            return self.getNext().gnscRec(f, len, diff, speed, dist)
        
    def getTrainData(self)->list:
        """Get a list of data points from each train
        I plan to add more, for now just the states"""
        states = []
        for t in self._trains:
            states.append(t.getState())

        return states
    
    def __str__(self)->str:
        return f"Track {self._id} is a {type(self)}"

class Intersection(Track):
    def __init__(self, id=-1, len=0, speedLimit=44, times:list[float] = [10, 10]):
        """Times: Even indeces = Go, Odd = Stop"""
        super().__init__(id, len, speedLimit)
        self._times = times
        self._stopped = False
        self._timer = self._times[0]
        self._timeIndex = 0
    
    def tick(self)->None:
        """Instructions for each second"""

        #NOTE: Make slightly more efficient
        self._timer-=1
        if self._timer <= 0:
            self._stopped = not self._stopped
            self._timeIndex += 1
            if self._timeIndex >= len(self._times):
                self._timeIndex = 0
            self._timer = self._times[self._timeIndex]
        
        # if self._stopped:
        #     print("STOP")
        # else:
        #     print("GO")
        
        self._next.tick()
        # if self._id=="why":
        #     print(self._stopped)
    
    def setTimes(self, times:list[float])->None:
        """Set the times for the intersection. Only cares about times for the train.
        First time should be for train to be going, second should be stop."""
        self._times = times
    
    def gnscRec(self, f:Callable[[float],tuple[float,float]], len:float, diff:float, speed:float, dist:float)->tuple[float, float]:
        """Recursive helper function for getNextSpeedChange()"""
        
        #If needs to stop, add stop
        if speed == None or speed != 0:
            if self._stopped or self._timer <= 4:
                min, max = f(0)
                #print(f"{min:.2f}, {len:.2f}, {max:.2f}")
                if min <= len and max >= len:
                    newDiff = len - min
                    # if self._id == "dei2":
                    #     print(newDiff)
                    if newDiff > diff:
                        if len > 500:
                            return 0, len #NOTE: For a speed of 0, not necessary to continue recursion?
                        else:
                            return self.getNext().gnscRec(f, len, newDiff, 0, len)
        
        #Otherwise add nothing
        if len > 500:
            return speed, dist
        return self.getNext().gnscRec(f, len, diff, speed, dist)
    
    def addTrain(self, train)->None:
        """Should be no trains on a track with no length"""
        if self._stopped:
            print(f"SKIPPED A RED WEEWOO: {self._times[self._timeIndex]-self._timer} OVER!!! ({self._id})")
        self.getNext().addTrain(train)
    
    def shuffleTimer(self):
        """Shuffles the timer to a random time"""
        timer = random.randint(1, sum(self._times))
        i = 0
        while timer > self._times[i]:
            timer -= self._times[i]
            i+=1
        
        self._timer = timer
        self._timeIndex = i
        self._stopped = (i%2 == 1)
        #print(self._times)
        


class Station(Track):
    def __init__(self, id=-1, len=150, speedLimit=44, boardTime:int = 10):
        super().__init__(id, len, speedLimit)
        self._boardTime = boardTime
    
    def tick(self):
        needsPopped = 0
        for t in self._trains:
            if t.hasBoarded():
                #Check for needed state of train
                speed, dist = self.getNextSpeedChange(t)
                if speed == None:
                    t.accelerate()
                else:
                    t.targetSpeed(dist, speed)

                t.tick()
                #print(t)

                #check if needs to move on
                if t.getPosition() > self._len:
                    needsPopped += 1
                    t.setPosition(t.getPosition()-self._len)
            
            else:
                if t.getState() == State.BOARD:
                    t.tick()
                else:
                    t.targetSpeed(self._len-5-t.getPosition(), 0)
                    _, s, _ = t.tick()
                    if s==0:
                        t.board(self._boardTime)
        
            #print(f"{t} at station {self._id}")

        self._next.tick()
        
        #trains should still be in order
        #NOTE: Make sure trains are in order
        for i in range(needsPopped):
            t = self._trains.pop()
            t._hasBoarded = False
            self._next.addTrain(t)
        

    
    def gnscRec(self, f:Callable[[float],tuple[float,float]], len:float, diff:float, speed:float, dist:float)->tuple[float, float]:
        """Recursive helper function for getNextSpeedChange()"""
        #Slow for station, should be plenty of time to reach lower speed
        if speed == None or self._speedLimit < speed:
            min, max = f(self._speedLimit)
            if min <= len and max >= len:
                newDiff = len - min
                # if self._id == "Englewood Avenue":
                #     print(newDiff)
                if newDiff > diff:
                    if len > 500:
                        return self._speedLimit, len
                    else:
                        return self.getNext().gnscRec(f, len+self._len, newDiff, self._speedLimit, len)
        
        
                
        
        # #If needs to stop, add stop
        # len+=self._len-20
    
        # min, max = f(0)
        # #print(f"{min:.2f}, {len:.2f}, {max:.2f}")
        # if min <= len and max >= len:
        #     newDiff = max - len
        #     if newDiff > diff:
        #         if len > 500:
        #             return 0, len
        #         else:
        #             return self.getNext().gnscRec(f, len, newDiff, 0, len)
        
        #Otherwise add nothing
        len+=self._len
        if len > 500:
            return speed, dist
        return self.getNext().gnscRec(f, len, diff, speed, dist)


class Start(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(id, len, speedLimit)
    
    def tick(self):
        self._next.tick()
    
    def addTrain(self, train):
        self._next.addTrain(train)


class End(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(id, len, speedLimit)
        self._finished = None
    
    def gnscRec(self, f:Callable[[float],tuple[float,float]], len:float, diff:float, speed:float, dist:float)->tuple[float, float]:
        """Recursive helper function for getNextSpeedChange()"""
        if speed == None or self._speedLimit < speed:
            min, max = f(self._speedLimit)
            if min <= len and max >= len:
                newDiff = len - min
                if newDiff > diff:
                    return self._speedLimit, len

        return speed, dist

    
    def addTrain(self, train):
        self._finished = train.getId()
        del train
    
    def tick(self):
        return None
    
    def getFinished(self):
        id = self._finished
        self._finished = None
        return id


