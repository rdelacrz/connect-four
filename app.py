"""
Starts the application.

Tested with CEF Python v66.1+
"""

# Built-in libraries
import platform
import os, sys

# Third-party libraries
from cefpython3 import cefpython as cef

def main():
    check_versions()
    sys.excepthook = cef.ExceptHook     # To shutdown all CEF processes on error

    cef.Initialize(settings={
        'context_menu': {
            'enabled': True,        # Enables right click menu within the application
        }
    })
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    browser = cef.CreateBrowserSync(url='file://' + os.path.join(curr_dir, "ui", "dist", "index.html"))
    cef.MessageLoop()
    cef.Shutdown()

def check_versions():
    ver = cef.GetVersion()
    print("[hello_world.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[hello_world.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "66.1", "CEF Python v66.1+ required to run this"

if __name__ == '__main__':
    main()
