import context
from path.path import PATH_TYPE

def test_path():
    assert PATH_TYPE.DIRECTORY != None
    assert PATH_TYPE.FILE != None