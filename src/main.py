from genericpath import isfile
import sys
import os.path as path
from document.document import SUPPORTED_DOCUMENTS
from app.app import App
from path.path import PATH_TYPE

def main():
    num_args = len(sys.argv)

    # check for exactly one command line argument
    if (num_args > 2):
        raise ValueError(f"The program expects exactly one argument but {num_args - 1} were specified")

    # extract path
    PATH = sys.argv[1]

    # check if the path points to correct location and determine if it is a file of a directory
    TYPE = None
    if (path.isfile(PATH)): TYPE = PATH_TYPE.FILE
    elif (path.isdir(PATH)): TYPE = PATH_TYPE.DIRECTORY
    else:
        raise FileNotFoundError("Invalid Path")

    # process the document
    app = App(PATH, TYPE)
    app.run()


if __name__ == "__main__":
    main()