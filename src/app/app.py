import context
from os import path, listdir
from os.path import isfile
from os.path import dirname, basename
from warnings import WarningMessage
from document.jpg import JPG
from document.png import PNG
from path.path import PATH_TYPE
from document.document import SUPPORTED_DOCUMENTS
import pandas as pd

EXTENSION_MAP = {
    '.jpg': JPG, 
    '.png': PNG
}

class App:
    def __init__(self, path, category):
        files = []

        if (category == PATH_TYPE.FILE):

            if (self.__supports_extension(path)):
                files.append(path)
            else:
                raise ValueError(f"The type of file {path} is not supported\nUse {' '.join(SUPPORTED_DOCUMENTS)} instead")
        
        elif (category == PATH_TYPE.DIRECTORY):
            for f in listdir(path):
                
                if not isfile(''.join(path, f)):
                    raise WarningMessage(f"Ignoring subdirectory {f} in the given directory")
                    continue

                else:
                    if (self.__supports_extension(f)):
                        files.append(''.join(path, f))
                    else:
                        raise WarningMessage(f"Type not supported. Skipping file {''.join(path, f)}")

        self.files = files
            
    def __supports_extension(self, filename):        
        if (self.__get_extension(filename) not in SUPPORTED_DOCUMENTS):
            return False
        return True

    def __get_extension(self, filename):
        return path.splitext(filename)[1]

    def run(self):

        output = pd.DataFrame(columns = ["title", "authors", "publishers", "isbn"])

        for f in self.files:
            info = EXTENSION_MAP[self.__get_extension(f)](f).info
            output.loc[len(output.index)] = [
                info['title'],
                '\n'.join(info['authors']),
                '\n'.join(info['publishers']),
                info['isbn']
            ]


        try:
            writer = pd.ExcelWriter(f"{dirname(self.files[0])}/output.xlsx", engine='openpyxl')
            output.to_excel(writer, sheet_name = f'{basename(self.files[0])}', encoding='utf8')
            writer.save()
        except IndexError:
            pass