from multiprocessing.sharedctypes import Value
import context
from app.app import App
from path.path import PATH_TYPE
from os import listdir, remove
from os.path import dirname

def test_file():
    App('test/assets/clean-code.jpg', PATH_TYPE.FILE).run(f'{dirname(__file__)}/test_output.xlsx')
    assert "test_output.xlsx" in listdir(dirname(__file__))
    remove(f'{dirname(__file__)}/test_output.xlsx')

def test_directory():
    App('test/assets/pictures', PATH_TYPE.DIRECTORY).run(f'{dirname(__file__)}/test_output.xlsx')
    assert "test_output.xlsx" in listdir(dirname(__file__))
    remove(f'{dirname(__file__)}/test_output.xlsx')

def test_support():
    filename = 'test/assets/clean-code.pdf'
    try:
        App(filename, PATH_TYPE.FILE)
        assert False
    except ValueError:
        assert True