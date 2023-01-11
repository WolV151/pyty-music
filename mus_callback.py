from threading import Thread


class SearchResultThread(Thread):

    def __init__(self, callback, name="result-pick-thread"):
        self.callback = callback
        super(SearchResultThread, self).__init__(name=name)
        self.start()

    def run(self):
        self.callback()


class SearchInputThread(Thread):

    def __init__(self, callback, name="keyboard-thread"):
        self.callback = callback
        super(SearchInputThread, self).__init__(name=name)
        self.start()

    def run(self):
        while ...:
            self.callback(input("Search..: "))
