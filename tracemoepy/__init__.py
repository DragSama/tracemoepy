"""Import all the classes."""

from .tracemoe import TraceMoe
from .errors import *

__author__ = ["DragSama"]
__version__ = 0.6

if __name__ == '__main__':
  from pprint import pprint
  pprint(__author__, __version__, TraceMoe)
