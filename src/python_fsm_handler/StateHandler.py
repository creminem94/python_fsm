from typing import List, Callable
from enum import Enum
import time

class StateLink():
    def __init__(self, nextState: Enum, condition: Callable) -> None:
        self.nextState = nextState
        self.condition = condition
    
    def test(self):
        return self.condition()

    def getNext(self):
        return self.nextState

class StateObject():
    def __init__(self, 
            state: Enum,
            stateLinks: List[StateLink],
            pre: Callable = lambda: None, 
            exec: Callable = lambda: None, 
            post: Callable = lambda: None) -> None:
        self.state = state
        self.stateLinks = stateLinks
        self.pre = pre
        self.exec = exec
        self.post = post

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Enum):
            return other == self.state
        if isinstance(other, self.__class__):
            return other.state == self.state

        return False

class FsmHandler():
    def __init__(self, states: List[StateObject], firstState: Enum, loopSleep: float = 0, loopCallback = None, logger = None) -> None:
        self.logger = logger
        self.states = states
        self.currentState = None
        self.changeState(firstState)
        self.loopSleep = loopSleep
        self.loopCallback = loopCallback

        while True:
            self.loop()

    def loop(self):
        self.currentState.exec()
        self.checkCondition()
        time.sleep(self.loopSleep)
        # TODO, should check if the callback has the exact number of params
        if callable(self.loopCallback):
            self.loopCallback(self.currentState.state.name)


    def getState(self, state: Enum):
        for s in self.states:
            if s == state:
                return s

        return None

    def checkCondition(self):
        for stateLink in self.currentState.stateLinks:
            if stateLink.test():
                self.changeState(stateLink.getNext())
                return

    def changeState(self, state: Enum):
        #first execute the post function of prev state
        if self.currentState is not None:
            self.currentState.post()

        self.currentState = self.getState(state)
        if self.currentState is None:
            raise Exception('State not implemented')
        if self.logger is not None:
            self.logger('new state: %r' % state)
        #execute the pre function of the new state
        self.currentState.pre()
    