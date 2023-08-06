from startme import StartMe

class StartMeExampleBoot(StartMe):
    def on_start(self):
        print(self.__class__.__name__, "started")
