from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def run_test(self, code_change):
        pass
