from train import TrainQueue, Train, State
import time


class Track:
    def __init__(self, id=-1, len=1000, speedLimit=44):
        self._trains:TrainQueue = TrainQueue()
        self._next:Track = None
        self._len = len
        self._speedLimit = speedLimit
        self._id = id

    def tick(self):
        """Instructions for each second"""
        for t in self._trains:
            t.accelerate()
            t.tick()
            print(t)

    def getNext(self)->'Track':
        """Get next track"""
        return self._next

    def setNext(self, next:'Track')->None:
        """Set next track"""
        self._next = next
    
    def addTrain(self, train:Train)->None:
        """Add train to this track segment"""
        self._trains.add(train)
    
    def getNextSpeedChange(self, len:int=None)->list[list[float, float]]:
        """Returns the speed of and distance to the next speed change"""
        if len==None:
            len = self._len
        else:
            len += self._len
        if len > 500:
            return []
        return self._next.getNextSpeedChange(len)


class Intersection(Track):
    def __init__(self, id=-1, len=0, speedLimit=44, times:list[float] = [10, 10]):
        super().__init__(len, id, len, speedLimit)
        self._times = times
        self._stopped = False
        self._timer = self._times[0]
        self._timeIndex = 0
    
    def tick(self)->None:
        """Instructions for each second"""

        #NOTE: Make slightly more efficient
        self._timer-=1
        if self._timer == 0:
            self._timeIndex += 1
            if self._timeIndex == len(self._times):
                self._timeIndex = 0
            self._timer = self._times[self._timeIndex]
    
    def setTimes(self, times:list[float])->None:
        """Set the times for the intersection. Only cares about times for the train.
        First time should be for train to be going, second should be stop."""
        self._times = times
    
    def getNextSpeedChange(self, len:int = None)->list[list[float, float]]:
        """Returns the speed of and distance to the next speed change"""
        if len==None:
            len = self._len
        else:
            len += self._len
        
        #If needs to stop, add stop
        if self._stopped or self._timer < 3:
            if len > 500:
                return [[0, len]]
            else:
                return self._next.getNextSpeedChange(len).append([0, len])
        
        #Otherwise add nothing
        else:
            if len > 500:
                return []
            return self._next.getNextSpeedChange(len)
    
    def addTrain(self, train)->None:
        """Should be no trains on a track with no length"""
        self.getNext().addTrain(train)


class Station(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(len, id, len, speedLimit)

class Start(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(len, id, len, speedLimit)

class End(Track):
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(len, id, len, speedLimit)


def main():
    track = Track(100000)
    track.addTrain(Train(6969))

    while True:
        track.tick()
        time.sleep(.2)


main()