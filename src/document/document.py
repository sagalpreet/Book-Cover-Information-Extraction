from abc import ABC, abstractmethod

SUPPORTED_DOCUMENTS = ['jpg', 'png']

class Document(ABC):
    @abstractmethod
    def __init__(self):
        self.__content = None
        self.__info = {}
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def __parse(self):
        pass

    @abstractmethod
    def __extract(self):
        pass
    
    @property
    def info(self):
        return self.info