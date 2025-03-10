from enum import Enum
import warnings

ACC = 4.1
DEC = 5.1
INVACC = 1/ACC

class State(Enum):
    TARGET = 0
    ACCELERATE = 1
    BOARD = 2
    PENDING = 3


def stateToString(s:State)->str:
    """Turns a state into its action string i.e.\n
    BOARD->Boarding"""
    if s==State.TARGET:
        return "Targetting"
    elif s==State.ACCELERATE:
        return "Accelerating"
    elif s==State.BOARD:
        return "Boarding"
    elif s==State.PENDING:
        return "Waiting for State"
    else:
        return "Unknown"



class Train:
    def __init__(self, id=0, maxSpeed:float=44): #max speed, and all speeds, in feet/sec
        self._id = id
        self._state = State.TARGET

        self._speed:float = 0
        self._maxSpeed:float = maxSpeed
        self._position:float = 0
        
        self._targetSpeed:float = 0
        self._targetDist:float = 0
        
        self._boardTimer:int = 0
        self._hasBoarded:bool = False

        
        
    
    def minTargetDist(self) -> float:
        """Get the distance when the train will decelerate to match a target speed. \n
        Uses acceleration value to naively deal with smooth->discrete innacuracies"""
        return (self._targetSpeed**2-self._speed**2)*.5*INVACC
    

    def tick(self)-> tuple[State, float, float]:
        """Perform basic logic on speed and some miscelanious values\n
        Returns train state at the end, its speed, and its position"""

        #warn in untouched pending
        if self._state==State.PENDING:
            warnings.warn("Train left PENDING on tick call",RuntimeWarning)



        #Boarding logic
        elif self._state == State.BOARD:
            self._boardTimer -= 1
            if self._boardTimer <= 0:
                self._state = State.PENDING
        



        #Acceleration Logic
        elif self._state == State.ACCELERATE:
            if self._speed < self._maxSpeed - ACC:
                self._speed += ACC
            else:
                self._speed = self._maxSpeed
            
            self._position+=self._speed


        #Target Speed logic
        elif self._state == State.TARGET:
            
            #If we should decelerate
            if self._targetSpeed < self._speed:
                if self.minTargetDist() <= self._targetDist:
                    if self._speed > DEC:
                        self._speed -= DEC
                    else: self._speed = 0
                
                #accelerate unless it's close 
                elif self.minTargetDist > self._targetDist+40: ###NOTE Value subject to change
                    if self._speed < self._maxSpeed - ACC:
                        self._speed += ACC
                    else:
                        self._speed = self._maxSpeed
            
            #elif we can go above target speed
            elif self._targetDist > 40: ###NOTE Value subject to change
                if self._speed < self._maxSpeed - ACC:
                    self._speed += ACC
                else:
                    self._speed = self._maxSpeed
            
            #elif we should treat target speed as max
            elif self._speed < self._targetSpeed:
                if self._speed < self._targetSpeed - ACC:
                    self._speed += ACC
                else:
                    self._speed = self._targetSpeed
            
            self._position+=self._speed
            self._targetDist-=self._speed

        
        return self._state, self._speed, self._position #true for either stopping or boarding
            

    
    def targetSpeed(self, dist:float, speed:float=0)->None:
        """Tells the train to target a speed at a certain distance away"""
        self._state = State.TARGET
        self._targetDist = dist
        self._targetSpeed = speed

    def accelerate(self)->None:
        """Tells the train to accelerate to its max speed until told otherwise"""
        self._state = State.ACCELERATE

    def board(self, t:float)->None:
        """Tells the train to board passengers for time t"""
        self._state = State.BOARD
        self._boardTimer = t
        self._hasBoarded = True

    def setMaxSpeed(self, speed:float)->None:
        """Set the max speed of the train on a type of track"""
        self._maxSpeed = speed

    def getId(self):
        """Returns train's ID"""
        return self._id
    
    def hasBoarded(self)->bool:
        """Return true if train has boarded at this track segment"""
        return self._hasBoarded

    def getSpeed(self)->float:
        """Get the current speed of the train"""
        return self._speed
    
    def getPosition(self)->float:
        """Get the current position of the train"""
        return self._position
    
    def __str__(self)->str:
        s =  f"Train {self._id} at position {self._position:.2f} is {stateToString(self._state)}. "
        if self._state ==State.BOARD:
            s+= f"Waiting {self._boardTimer} seconds."
        else:
            s+= f"Going {self._speed:.2f} ft/s."
        return s



class TQNode:
    def __init__(self, t:Train):
        self._train:Train = t
        self._next:TQNode = None
        self._prev:TQNode = None
    
    def getNext(self)->'TQNode':
        return self._next
    
    def setNext(self, n:'TQNode')->None:
        self._next=n
    
    def getPrev(self)->'TQNode':
        return self._prev

    def setPrev(self, n:'TQNode')->None:
        self._prev = n
    
    def getTrain(self)->Train:
        return self._train

class TrainQueue:
    def __init__(self):
        self._start:TQNode = None
        self._end:TQNode = None
        self._len = 0
        self._iterNode:TQNode = None

    def add(self, t:Train)->None:
        """Add a train to the back of the queue\n
        Yes this isn't the proper terminology but i hate the word 'enqueue' so shut up"""
        n = TQNode(t)
        if self._len==0:
            self._start = n
            self._end = n
        
        else:
            n.setNext(self._end)
            self._end.setPrev(n)
            self._end = n
        
        self._len +=1
    
    def pop(self)->Train:
        """Pop a train off the front of the queue\n
        Yes this isn't the proper terminology but i hate the word 'dequeue' so shut up"""
        if self._len==0:
            return None
        
        n = self._start
        if self._len == 1:
            self._start = None
            self._end = None
        else:
            self._start = n.getPrev()
            self._start.setNext(None)
        self._len-=1
        return n
    

    #Iterability so I can go through items easily later
    def __iter__(self):
        self._iterNode = self._start
        return self
    
    def __next__(self):
        if not self._iterNode:
            raise StopIteration
        n = self._iterNode
        self._iterNode = n.getPrev()
        return n.getTrain()