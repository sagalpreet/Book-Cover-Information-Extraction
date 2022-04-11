from abc import ABC, abstractmethod

SUPPORTED_DOCUMENTS = ['jpg', 'png']

class Document(ABC):
    @abstractmethod
    def __init__(self):
        self.content = None
        self.extracted_information = {}
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def parse(self):
        pass
    
    @property
    def extracted_information(self):
        return self.extracted_information