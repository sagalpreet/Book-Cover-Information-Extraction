import context
from document.jpg import JPG

def test_jpg():
    info = JPG('test/assets/clean-code.jpg').info
    assert(len(info) == 4)