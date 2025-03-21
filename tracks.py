from train import TrainQueue, Train, State
from collections.abc import Callable
import time


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
            print(t)

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
        len+=self._len
        if len > 500:
            return speed, dist
        else:
            return self.getNext().gnscRec(f, len, diff, speed, dist)


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
        if self._timer == 0:
            self._stopped = not self._stopped
            self._timeIndex += 1
            if self._timeIndex == len(self._times):
                self._timeIndex = 0
            self._timer = self._times[self._timeIndex]
        
        # if self._stopped:
        #     print("STOP")
        # else:
        #     print("GO")
        
        self._next.tick()
    
    def setTimes(self, times:list[float])->None:
        """Set the times for the intersection. Only cares about times for the train.
        First time should be for train to be going, second should be stop."""
        self._times = times
    
    def gnscRec(self, f:Callable[[float],tuple[float,float]], len:float, diff:float, speed:float, dist:float)->tuple[float, float]:
        """Recursive helper function for getNextSpeedChange()"""
        
        #If needs to stop, add stop
        if self._stopped or self._timer < 3:
            min, max = f(0)
            #print(f"{min:.2f}, {len:.2f}, {max:.2f}")
            if min <= len and max >= len:
                newDiff = max - len
                if newDiff > diff:
                    if len > 500:
                        return 0, len
                    else:
                        return self.getNext().gnscRec(f, len, newDiff, 0, len)
        
        #Otherwise add nothing
        if len > 500:
            return speed, dist
        return self.getNext().gnscRec(f, len, diff, speed, dist)
    
    def addTrain(self, train)->None:
        """Should be no trains on a track with no length"""
        self.getNext().addTrain(train)


class Station(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(id, len, speedLimit)

class Start(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(id, len, speedLimit)

class End(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(id, len, speedLimit)
    
    def gnscRec(self, f:Callable[[float],tuple[float,float]], len:float, diff:float, speed:float, dist:float)->tuple[float, float]:
        """Recursive helper function for getNextSpeedChange()"""
        return speed, dist
    
    def addTrain(self, train):
        del train
    
    def tick(self):
        return None


def main():
    track = Track(len=500)
    i1 = Intersection(times=[5,30])
    t2 = Track(len=500)
    i2 = Intersection(times=[5,30])
    tEnd = End()
    track.setNext(i1)
    i1.setNext(t2)
    t2.setNext(i2)
    i2.setNext(tEnd)
    track.addTrain(Train(6969))

    while True:
        track.tick()
        time.sleep(.2)


main()