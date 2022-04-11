from document import Document

class JPG(Document):
    def __init__(self, path: str = None):
        if (path):
            self.content = self.read(path)
        else:
            self.content = None
            
        self.extracted_information = {}
        
    def read(self, path: str):
        '''
        TODO: read jpg content from path
        '''
        pass
    
    def parse(self):
        '''
        TODO: parse content and store information
        in extracted_information dictionary
        '''
        pass