from startme import StartMe
from datetime import datetime, timedelta
import time


class Ticker(StartMe):

    def __init__(self):
        super().__init__()
        self.period = 10

    def on_schedule(self) -> None:
        print(datetime.now().strftime("%H:%M:%S"), self.__class__.__name__, "tick", self.period)
    
    def reschedule(self):
        return time.time() + self.period

class Ticker1min(Ticker):
    def __init__(self):
        super().__init__()
        self.period = 60
