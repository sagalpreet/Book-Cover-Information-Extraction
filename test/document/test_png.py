import context
from document.png import PNG

def test_png():
    info = PNG('test/assets/clean-code.jpg').info
    assert(len(info) == 4)