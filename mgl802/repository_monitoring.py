class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

class RepositoryMonitor:
    def __init__(self, kernel):
        self.kernel = kernel

    def detect_code_change(self):
        # Logic to detect new commits or pull requests
        code_change = self.get_code_change()
        self.kernel.initiate_testing(code_change)

    def get_code_change(self):
        # Retrieve details of the code change
        return {"code": "new code changes"}
