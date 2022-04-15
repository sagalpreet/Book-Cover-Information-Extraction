import pandas as pd
import context
from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def extract(content: pd.DataFrame, confidence = 0):
        pass