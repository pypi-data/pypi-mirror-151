class StartMe():
    onstart = False
    def __init__(self):
        pass

    def run(self):
        print("run", self)

    def __repr__(self):
        return type(self).__name__
