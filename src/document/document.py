from abc import ABC, abstractmethod

SUPPORTED_DOCUMENTS = ['.jpg', '.png']

class Document(ABC):
    @abstractmethod
    def __init__(self):
        self.__content = None
        self.info = {}
    
    @abstractmethod
    def read(self):
        pass