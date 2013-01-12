# Updates sys.path to contain the parent folder (ncss132); pretend we're in a package.
if not __package__:
  import sys, os
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
  import dbapi; __package__ = 'dbapi'

