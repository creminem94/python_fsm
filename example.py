from python_fsm_handler.StateHandler import FsmHandler, StateLink, StateObject
from enum import Enum


moveCounter = 0
workCounter = 0

class FsmState(Enum):
    MOVE = 0
    WORK = 1
def test():

    def movePre():
        print("move pre")

    def moveExec():
        print("move exec")
        global moveCounter
        moveCounter += 1

    def movePost():
        print("move post")
        global moveCounter
        moveCounter = 0

    def workPre():
        print("work pre")
    
    def workExec():
        print("work exec")
        global workCounter
        workCounter += 1
    
    def workPost():
        print("work post")
        global workCounter
        workCounter = 0

    def loopCallback(state):
        print(f"loopCallback: {state}")
        print(f"moveCounter: {moveCounter}")
        print(f"workCounter: {workCounter}")
    def moveToWork():
        return moveCounter >= 5
    
    def workToMove():
        return workCounter >= 5

    states = [
        StateObject(FsmState.MOVE, [
            StateLink(FsmState.WORK, moveToWork)
        ], movePre, moveExec, movePost),
        StateObject(FsmState.WORK, [
            StateLink(FsmState.MOVE, workToMove)
        ], workPre, workExec, workPost),
    ]

    FsmHandler(states, FsmState.MOVE, logger=print, loopCallback=loopCallback)


if __name__ == "__main__":
    test()