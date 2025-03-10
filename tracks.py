from train import TrainQueue, Train, State
import time


class Track:
    def __init__(self, id=-1, len=1000, speedLimit=44):
        self._trains:TrainQueue = TrainQueue()
        self._next:Track = None
        self._len = len
        self._speedLimit = 44
        self._id = id

    def tick(self):
        for t in self._trains:
            t.accelerate()
            t.tick()
            print(t)

    def getNext(self)->'Track':
        return self._next

    def setNext(self, next:'Track')->None:
        self._next = next
    
    def addTrain(self, train:Train)->None:
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
    def __init__(self, id=-1, len=0, speedLimit=44):
        super().__init__(len, id, len, speedLimit)


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