from tracks import *
from train import Train

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


    start.addTrain(Train(1))
    while True:
        start.tick()
        timer += 1
        id = end.getFinished()
        if id:
            print(f"Train {id} finished in {timer//60}:{timer%60}")
            timer = 0
            start.addTrain(Train(int(id)+1))

        # time.sleep(.02)


main()