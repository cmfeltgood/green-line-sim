from tracks import *
from train import Train

def strTime(sec: int)->str:
    return f"{sec//60}:{sec%60}"


class dataCollector:
    def __init__(self):
        self._stateFreqs = {State.TARGET: 0, State.ACCELERATE: 0, State.BOARD:0, State.PENDING:0}
    

def shuffleTimers(t: Track):
    while t.getNext():
        if type(t) == Intersection:
            t.shuffleTimer()
        t = t.getNext()


def main():
    start: Start = None
    end: End = None

    f = open("outbound_observed.csv", "r")
    lines = f.readlines()

    curr: Track = Start()

    for i in range(1, len(lines)):
        atts = lines[i].split(",")
        type = atts[0]
        print(f"{i}, {atts}")

        if type == "Start":
            start = Start(id=atts[2])
            curr = start
        elif type == "Track":
            curr.setNext(Track(len=float(atts[1]), id=atts[2], speedLimit=float(atts[3])))
            curr = curr.getNext()
        elif type == "Intersection":
            curr.setNext(Intersection(id=atts[2], times=[float(atts[4]), float(atts[5])]))
            curr = curr.getNext()
        elif type == "Station":
            curr.setNext(Station(len=float(atts[1]), id=atts[2], speedLimit=float(atts[3]), boardTime=int(atts[6])))
            curr = curr.getNext()
        elif type == "End":
            curr.setNext(End(id=atts[2]))
            end = curr.getNext()
            break


    print("File Imported")
    timer = 0
    times = []

    id = None
    start.addTrain(Train(1))
    shuffleTimers(start)


    while id != 1001:
        start.tick()
        timer += 1
        id = end.getFinished()
        if id:
            times.append(timer)
            print(f"Train {id} finished in {timer//60}:{timer%60}")
            # times.sort()
            # print(f"Min: {strTime(times[0])}, 10%: {strTime(times[len(times)//10])}, Med: {strTime(times[len(times)//2])}, 90%: {strTime(times[len(times)-len(times)//10-1])}, Max: {strTime(times[-1])}")
    
            timer = 0
            start.addTrain(Train(int(id)+1))
            shuffleTimers(start)


        # time.sleep(.02)
    

    times.sort()
    print(f"Min: {strTime(times[0])}, 10%: {strTime(times[len(times)//10])}, Med: {strTime(times[len(times)//2])}, 90%: {strTime(times[len(times)-len(times)//10])}, Max: {strTime(times[-1])}")
    



main()