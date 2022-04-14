import context
from document.document import Document
import pytesseract
from PIL import Image, ImageFilter
import numpy as np
from io import StringIO
import pandas as pd
from extractor.heuristic_extractor import Heuristic_Extractor

class JPG(Document):
    def __init__(self, path: str = None):
        self.__content = None
        self.info = {}

        if (path):
            self.read(path)
        else:
            self.__path = None
        
    def read(self, path: str):
        '''
        store path
        '''
        self.__path = path
        self.__parse()
        self.__extract()
    
    def __parse(self):
        '''
        parse file and store information
        in content
        '''
        path = self.__path

        try:
            img = Image.open(path).convert('L')
        except:
            raise FileNotFoundError("Invalid Path")

        self.__content = pd.read_csv(StringIO(pytesseract.image_to_data(img)), sep='\t')
        
    def __extract(self):
        self.info = Heuristic_Extractor.extract(self.__content)