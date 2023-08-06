import os
import wx

try:
    from ..PyTranslate import *
    from ..PyParams import Wolf_Param
except:
    from wolfhece.PyTranslate import *
    from wolfhece.PyParams import Wolf_Param

def main():
    ex = wx.App()
    frame = Wolf_Param(None,"Params")
    ex.MainLoop()

if __name__=="__main__":
    main()