from document import Document
import pytesseract
from PIL import Image, ImageFilter
import numpy as np
from io import StringIO
import pandas as pd
import context
from extractor.extractor import Extractor

class JPG(Document):
    def __init__(self, path: str = None):
        if (path):
            self.__path = self.read(path)
            self.__extract()
        else:
            self.__path = None
            self.__content = None
            self.__info = {}
        
    def read(self, path: str):
        '''
        store path
        '''
        self.__path = path
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
        self.__info = Extractor.heuristic_extract((self.__content))