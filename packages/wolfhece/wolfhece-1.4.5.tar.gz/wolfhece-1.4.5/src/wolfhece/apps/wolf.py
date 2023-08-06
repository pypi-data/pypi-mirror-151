import os
import wx
try:
    from ..PyTranslate import *
    from ..PyGui import MapManager
except:
    from wolfhece.PyTranslate import *
    from wolfhece.PyGui import MapManager

def main():
    ex = wx.App()
    mywolf=MapManager()
    ex.MainLoop()

if __name__=='__main__':
    main()