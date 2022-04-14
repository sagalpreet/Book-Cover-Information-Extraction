import pandas as pd
import context
from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def extract(content: pd.DataFrame, confidence = 50):
        pass

    @abstractmethod
    def __clean_dataframe(df: pd.DataFrame, confidence):
        pass

    @abstractmethod
    def __get_title(df: pd.DataFrame):
        pass

    @abstractmethod
    def __get_authors(df: pd.DataFrame):
        pass

    @abstractmethod
    def __get_publishers(df: pd.DataFrame):
        pass

    @abstractmethod
    def __get_isbn(df: pd.DataFrame):
        pass