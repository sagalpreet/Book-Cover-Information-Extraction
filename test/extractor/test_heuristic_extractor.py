import context
from document.jpg import JPG
from extractor.heuristic_extractor import Heuristic_Extractor
import pandas as pd

def get_info(path):
    df = JPG(path)._JPG__content
    info = Heuristic_Extractor.extract(df)
    return info

def test_heuristic_extractor_1():
    info = get_info('test/assets/clean-code.jpg')
    assert info['title'] == 'Clean Code'

def test_heuristic_extractor_2():
    info = get_info('test/assets/halliday.jpg')
    assert info['publishers'] == ['Wiley']

def test_valid_name():
    f = Heuristic_Extractor._Heuristic_Extractor__get_authors
    assert f(pd.DataFrame({'height': [], 'text': [], 'block_num': []})) == []

def test_empty_title():
    f = Heuristic_Extractor._Heuristic_Extractor__get_title
    assert f(pd.DataFrame({'height': [], 'text': [], 'block_num': []})) == ""
